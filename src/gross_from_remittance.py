"""
Compute gross pay given a tax year and total payroll tax remitted to CRA.

Payroll remittance = federal income tax + provincial income tax (Ontario)
                    + CPP employee contribution + EI employee premium.

Assumes employment income only (no RRSP, other income, or deductions).
Uses binary search to invert the remittance function.
"""

import argparse
import sys
from pathlib import Path

# Allow running as script when invoked from project root or src
sys.path.insert(0, str(Path(__file__).resolve().parent))

from individual import IndividualRevenue


# EI: rate per $100 of insurable earnings; max insurable earnings (annual)
# Source: CRA / ESDC (outside Quebec)
_EI_BY_YEAR = {
    2023: {"rate_per_100": 1.63, "max_insurable": 61_500},
    2024: {"rate_per_100": 1.66, "max_insurable": 63_200},
    2025: {"rate_per_100": 1.64, "max_insurable": 65_700},
}


def _ei_contribution(employment_income: float, year: int) -> float:
    """EI employee premium for the year (outside Quebec)."""
    if year not in _EI_BY_YEAR:
        raise ValueError(f"EI not configured for year {year}. Supported: {list(_EI_BY_YEAR)}")
    cfg = _EI_BY_YEAR[year]
    rate = cfg["rate_per_100"] / 100.0
    insurable = min(employment_income, cfg["max_insurable"])
    return insurable * rate


def total_payroll_remittance(gross: float, year: int) -> float:
    """
    Total payroll tax remitted to CRA for the given gross employment income and year.
    Equals federal tax + provincial tax + CPP + EI.
    """
    rev = IndividualRevenue(year)
    tr = rev.compute_basic_return(
        employment_income=gross,
        ucc_benefit=0.0,
        ei_benefits=0.0,
        investment_income=0.0,
        rrsp_contribution=0.0,
        medical_expenses=0.0,
        self_employed=False,
    )
    ei = _ei_contribution(gross, year)
    return tr.net_federal_tax + tr.provincial_tax + tr.cpp_contribution + ei


def gross_from_remittance(
    total_remitted: float,
    year: int,
    *,
    low: float = 0.0,
    high: float = 1_000_000.0,
    tol: float = 1.0,
    max_iter: int = 100,
) -> float:
    """
    Estimate gross employment income that yields the given total payroll remittance.

    Uses binary search. Assumes remittance is increasing in gross (no RRSP/other inputs).
    """
    if total_remitted <= 0:
        return 0.0

    rev = IndividualRevenue(year)
    for _ in range(max_iter):
        mid = (low + high) / 2.0
        if mid <= 0:
            return 0.0
        rem = total_payroll_remittance(mid, year)
        if abs(rem - total_remitted) <= tol:
            return round(mid, 2)
        if rem < total_remitted:
            low = mid
        else:
            high = mid
    return round((low + high) / 2.0, 2)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compute gross pay from total payroll tax remitted to CRA."
    )
    parser.add_argument(
        "remitted",
        type=float,
        help="Total payroll tax remitted to CRA (federal + provincial + CPP + EI)",
    )
    parser.add_argument(
        "year",
        type=int,
        nargs="?",
        default=2024,
        help="Tax year (default: 2024)",
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Print remittance breakdown for the computed gross",
    )
    args = parser.parse_args()

    if args.remitted < 0:
        print("Error: remitted amount must be non-negative.", file=sys.stderr)
        sys.exit(1)

    gross = gross_from_remittance(args.remitted, args.year)
    print(f"Year: {args.year}")
    print(f"Total remitted to CRA: ${args.remitted:,.2f}")
    print(f"Estimated gross pay:   ${gross:,.2f}")

    if args.verify:
        rem = total_payroll_remittance(gross, args.year)
        rev = IndividualRevenue(args.year)
        tr = rev.compute_basic_return(
            employment_income=gross,
            ucc_benefit=0.0,
            ei_benefits=0.0,
            investment_income=0.0,
            rrsp_contribution=0.0,
            medical_expenses=0.0,
            self_employed=False,
        )
        ei = _ei_contribution(gross, args.year)
        print()
        print("Verification (remittance breakdown at estimated gross):")
        print(f"  Federal tax:    ${tr.net_federal_tax:,.2f}")
        print(f"  Provincial tax: ${tr.provincial_tax:,.2f}")
        print(f"  CPP:            ${tr.cpp_contribution:,.2f}")
        print(f"  EI:             ${ei:,.2f}")
        print(f"  Total:          ${rem:,.2f}")


if __name__ == "__main__":
    main()
