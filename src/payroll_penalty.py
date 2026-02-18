import math
from dataclasses import dataclass


@dataclass
class Tax:
    month: str
    monthly_fed_tax: float
    total_owed: float
    penalty: float


def main():
    scenario = "2024"
    # scenario = "full"
    # scenario = "reduced"
    print(f"SCENARIO:  {scenario}")
    match scenario :
        case "2024":
            craig_monthly_tax, miki_monthly_tax = full_2024()
        case "full":
            craig_monthly_tax, miki_monthly_tax = full_income()
        case "reduced":
            craig_monthly_tax, miki_monthly_tax = reduced_income()
    run_scenario(craig_monthly_tax, miki_monthly_tax)



def full_2024():
    craig_salary = 100000
    miki_salary = 50000
    craig_annual_fed_tax = 19150.00
    craig_annual_prov_tax = 7162.42
    miki_annual_fed_tax = 7987
    miki_annual_prov_tax = 2556.529

    return calculate_scenario(craig_salary, craig_annual_fed_tax, craig_annual_prov_tax, miki_salary, miki_annual_fed_tax, miki_annual_prov_tax)


def full_income():
    craig_salary = 100000
    miki_salary = 50000
    craig_annual_fed_tax = 17565.05
    craig_annual_prov_tax = 7162.42
    miki_annual_fed_tax = 7500.0
    miki_annual_prov_tax = 2556.529

    return calculate_scenario(craig_salary, craig_annual_fed_tax, craig_annual_prov_tax, miki_salary, miki_annual_fed_tax, miki_annual_prov_tax)


def reduced_income():
    craig_salary = 93186.96
    miki_salary = 42421.44

    craig_annual_fed_tax = 16168.38
    craig_annual_prov_tax = 6508.14
    miki_annual_fed_tax = 6363.22
    miki_annual_prov_tax = 2142.28

    return calculate_scenario(craig_salary, craig_annual_fed_tax, craig_annual_prov_tax, miki_salary, miki_annual_fed_tax, miki_annual_prov_tax)


def calculate_scenario(craig_salary, craig_annual_fed_tax, craig_annual_prov_tax, miki_salary, miki_annual_fed_tax, miki_annual_prov_tax):
    craig_annual_tax = craig_annual_fed_tax + craig_annual_prov_tax
    craig_monthly_income = craig_salary / 12
    # craig_monthly_fed_tax = craig_annual_fed_tax / 12
    craig_monthly_tax = craig_annual_tax / 12

    miki_annual_tax = miki_annual_fed_tax + miki_annual_prov_tax
    miki_monthly_income = miki_salary / 12
    # miki_monthly_fed_tax = miki_annual_fed_tax / 12
    miki_monthly_tax = miki_annual_tax / 12

    print(f"\t\tAnnual\tMonthly\t\tFed Tax\t\tProv Tax\tTotal Tax")
    print(
        f"Craig\t{craig_salary}\t{craig_monthly_income:.2f}\t\t{craig_annual_fed_tax}\t\t{craig_annual_prov_tax}\t\t{craig_annual_tax:.2f}")
    print(
        f"Miki\t{miki_salary}\t{miki_monthly_income:.2f}\t\t{miki_annual_fed_tax}\t\t{miki_annual_prov_tax:.2f}\t\t{miki_annual_tax:.2f}")
    print("-" * 80)
    return craig_monthly_tax, miki_monthly_tax


def run_scenario(craig_monthly_fed_tax, miki_monthly_fed_tax):
    # months = [("april", 7), ("may", 6), ("june", 5), ("july", 4), ("august", 3), ("september", 2), ("october", 1), ("november", 0)]
    months = [("may", 6), ("june", 5), ("july", 4), ("august", 3), ("september", 2), ("october", 1), ("november", 0)]
    # months = [ ("june", 5), ("july", 4), ("august", 3), ("september", 2), ("october", 1), ("november", 0)]

    print("Craig's Back Taxes")
    craig_taxes = [calcuate_tax_owing(name, num_months_late, craig_monthly_fed_tax) for name, num_months_late in months]
    print()
    print("Miki's Back Taxes")
    miki_taxes = [calcuate_tax_owing(name, num_months_late, miki_monthly_fed_tax) for name, num_months_late in months]

    craig_original_owing = sum([x.monthly_fed_tax for x in craig_taxes])
    craig_total_owing = sum([x.total_owed for x in craig_taxes])
    craig_total_penalty = sum([x.penalty for x in craig_taxes])

    miki_original_owing = sum([x.monthly_fed_tax for x in miki_taxes])
    miki_total_owing = sum([x.total_owed for x in miki_taxes])
    miki_total_penalty = sum([x.penalty for x in miki_taxes])

    print("-" * 80)
    print("Craig")
    print(f"\tTotal original Fed Taxes:\t\t${craig_original_owing:,.2f}")
    print(f"\tTotal revised Fed Taxes:\t\t${craig_total_owing:,.2f}")
    print(f"\tTotal penalty incurred:\t\t\t${craig_total_penalty:,.2f}")
    print("Miki")
    print(f"\tTotal original Fed Taxes:\t\t${miki_original_owing:,.2f}")
    print(f"\tTotal revised Fed Taxes:\t\t${miki_total_owing:,.2f}")
    print(f"\tTotal penalty incurred:\t\t\t${miki_total_penalty:,.2f}")
    print()
    print("Total")
    print(f"\tTotal original Fed Taxes:\t\t${(craig_original_owing + miki_original_owing):,.2f}")
    print(f"\tTotal revised Fed Taxes:\t\t${(craig_total_owing + miki_total_owing):,.2f}")
    print(f"\tTotal penalty incurred:\t\t\t${(craig_total_penalty + miki_total_penalty):,.2f}")
    print("-" * 80)


def calcuate_tax_owing(name, num_months_late, monthly_fed_tax):
    penalty_rate = 0.10
    penalty = monthly_fed_tax * penalty_rate
    tax_plus_penalty = monthly_fed_tax + penalty

    interest_rate = 0.09

    P = tax_plus_penalty
    r = interest_rate
    n = 365
    t = (num_months_late / 12)
    total_owed = calculate_compound_interest(P, r, n, t)
    total_penalty = total_owed - monthly_fed_tax
    print(name)
    print(f"\tMonth tax owed:\t\t\t\t{monthly_fed_tax:.2f}")
    print(f"\tMonth tax + penalty:\t\t{tax_plus_penalty:.2f}")
    print(f"\ttax + penalty + interest:\t{total_owed:.2f}")
    print(f"\tTotal Penalty:\t\t\t\t{(total_penalty):.2f}")

    t = Tax(name, monthly_fed_tax, total_owed, total_penalty)
    return t


def calculate_compound_interest(P, r, n, t):
    A = P * math.pow((1 + (r / n)), n * t)
    return A


if __name__ == "__main__":
    main()
