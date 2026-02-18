"""
Driver module to calculate taxes owed for an individual or corporation
given a year and revenue/income. Callable from the command line.
"""

import argparse
from individual import IndividualRevenue
from corporate import CorporateRevenue
from data_objects import IndividualReturn


def calculate_individual_tax(year: int, income: float, **kwargs) -> IndividualReturn:
    """
    Calculate tax and contributions for an individual given year and income.
    Returns full IndividualReturn; use .total_tax_payable for tax owed.

    Optional kwargs (with defaults): ucc_benefit=0, ei_benefits=0,
    investment_income=0, rrsp_contribution=0, medical_expenses=0, self_employed=False.
    """
    rev = IndividualRevenue(year)
    ucc_benefit = kwargs.get("ucc_benefit", 0.0)
    ei_benefits = kwargs.get("ei_benefits", 0.0)
    investment_income = kwargs.get("investment_income", 0.0)
    rrsp_contribution = kwargs.get("rrsp_contribution", 0.0)
    medical_expenses = kwargs.get("medical_expenses", 0.0)
    self_employed = kwargs.get("self_employed", False)
    tr = rev.compute_basic_return(
        employment_income=income,
        ucc_benefit=ucc_benefit,
        ei_benefits=ei_benefits,
        investment_income=investment_income,
        rrsp_contribution=rrsp_contribution,
        medical_expenses=medical_expenses,
        self_employed=self_employed,
    )
    return tr


def _print_individual_breakdown(
    year: int,
    amount: float,
    tr: IndividualReturn,
    self_employed: bool,
) -> None:
    """Print detailed breakdown of individual taxes and contributions."""
    rev = IndividualRevenue(year)
    cpp_employee = rev.calculate_cpp(amount, self_employed=False)
    cpp_employer = tr.cpp_contribution - cpp_employee

    print(f"Individual tax (year {year}, income ${amount:,.2f}):")
    print()
    print("Income")
    print(f"  Employment income:     ${tr.employment_income:,.2f}")
    print(f"  Total income:          ${tr.total_income:,.2f}")
    print(f"  RRSP contribution:     ${tr.rrsp_contribution:,.2f}")
    print(f"  Taxable income:        ${tr.taxable_income:,.2f}")
    print()
    print("Income tax")
    print(f"  Federal income tax:    ${tr.net_federal_tax:,.2f}")
    print(f"  Provincial income tax: ${tr.provincial_tax:,.2f}")
    print(f"  Total income tax:      ${tr.total_tax_payable:,.2f}")
    print()
    print("CPP")
    print(f"  CPP1 (employee):       ${cpp_employee:,.2f}")
    if cpp_employer > 0:
        print(f"  CPP2 (employer):       ${cpp_employer:,.2f}")
    print(f"  Total CPP:             ${tr.cpp_contribution:,.2f}")
    print()
    total_with_cpp = tr.total_tax_payable + tr.cpp_contribution
    print("Summary")
    print(f"  Total (tax + CPP):     ${total_with_cpp:,.2f}")
    print(f"  After-tax income:      ${tr.after_tax_income:,.2f}")
    print(f"  Average tax rate:      {(tr.avg_tax_rate * 100):.2f}%")
    print(f"  Marginal tax rate:     {(tr.marginal_tax_rate * 100):.2f}%")


def calculate_corporate_tax(
    year: int,
    revenue: float,
    cpp_contributions: list[float] | None = None,
    deductions: float = 0.0,
    tax_credits: float = 0.0,
) -> float:
    """
    Calculate total tax payable for a corporation (CCPC) given year and revenue.

    Optional: cpp_contributions (list, default []), deductions (default 0), tax_credits (default 0).
    """
    rev = CorporateRevenue(year)
    cpp_contributions = cpp_contributions or []
    tr = rev.estimate_ccpc_tax(
        revenue=revenue,
        cpp_contributions=cpp_contributions,
        deductions=deductions,
        tax_credits=tax_credits,
    )
    return tr.total_tax_payable


def main():
    parser = argparse.ArgumentParser(
        description="Calculate taxes owed for an individual or corporation."
    )
    parser.add_argument(
        "entity",
        choices=["individual", "corporation"],
        help="Entity type: individual or corporation",
    )
    parser.add_argument(
        "year",
        type=int,
        help="Tax year (e.g. 2024)",
    )
    parser.add_argument(
        "amount",
        type=float,
        help="Income (individual) or revenue (corporation) in dollars",
    )
    parser.add_argument(
        "--rrsp",
        type=float,
        default=0.0,
        help="RRSP contribution (individual only)",
    )
    parser.add_argument(
        "--deductions",
        type=float,
        default=0.0,
        help="Business deductions (corporation only)",
    )
    parser.add_argument(
        "--tax-credits",
        type=float,
        default=0.0,
        help="Tax credits (corporation only)",
    )
    parser.add_argument(
        "--self-employed",
        action="store_true",
        help="Individual is self-employed (CPP2 employer portion applies)",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Print only the tax amount",
    )
    args = parser.parse_args()

    if args.entity == "individual":
        tr = calculate_individual_tax(
            args.year,
            args.amount,
            rrsp_contribution=args.rrsp,
            self_employed=args.self_employed,
        )
        if args.quiet:
            print(f"{tr.total_tax_payable:,.2f}")
        else:
            _print_individual_breakdown(
                args.year,
                args.amount,
                tr,
                self_employed=args.self_employed,
            )
    else:
        tax_owed = calculate_corporate_tax(
            args.year,
            args.amount,
            deductions=args.deductions,
            tax_credits=args.tax_credits,
        )
        if args.quiet:
            print(f"{tax_owed:,.2f}")
        else:
            print(f"Corporate tax (year {args.year}, revenue ${args.amount:,.2f}):")
            print(f"  Tax owed: ${tax_owed:,.2f}")


if __name__ == "__main__":
    main()
