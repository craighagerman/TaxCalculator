# from src.corporate import calculate_ccpc_taxable_revenue, calculate_ccpc_tax_reduction, CorporateRevenue
from src.corporate import CorporateRevenue
from src.data_objects import IndividualReturn, CorporateReturn, Income, BPA, Bracket
from src.individual import IndividualRevenue


############################################
# Put it all together
############################################
#
# def compute_basic_return(employment_income, ucc_benefit, ei_benefits, investment_income, rrsp_contribution,
#                          bpa_range, cpp_contribution, canada_employment_amount, medical_expenses,
#                          federal_brackets, provincial_brackets):
#     # Compute income
#     total_income = calculate_total_income(employment_income, ucc_benefit, ei_benefits, investment_income)
#     employment_deductions = calculate_employment_deductions(rrsp_contribution)
#     taxable_income = calculate_net_income(total_income, employment_deductions)
#     # TODO: compute cpp contribution here.
#     # Compute taxes on taxable income
#     basic_federal_tax = compute_federal_tax(taxable_income, federal_brackets)
#     provincial_tax = compute_provincial_tax(taxable_income, provincial_brackets)
#     marginal_tax_rate = _compute_margin_tax_rate(taxable_income, federal_brackets, provincial_brackets)
#     # Compute non-refundable tax credits
#     tax_credits = compute_non_refundable_tax_credits(taxable_income, bpa_range, federal_brackets,
#                                                      cpp_contribution, canada_employment_amount,
#                                                      ei_premiums, medical_expenses, taxable_income,
#                                                      fed_non_refundable_tax_credit_rate)
#     # Compute net federal tax
#     net_federal_tax = compute_net_federal_tax(basic_federal_tax, tax_credits)
#     # Total tax payable
#     total_tax_payable = net_federal_tax + provincial_tax
#     after_tax_income = employment_income - total_tax_payable
#     avg_tax_rate = total_tax_payable / employment_income
#     result = IndividualReturn(
#         employment_income=employment_income,
#         total_income=total_income,
#         taxable_income=taxable_income,
#         after_tax_income=after_tax_income,
#         rrsp_contribution=rrsp_contribution,
#         net_federal_tax=net_federal_tax,
#         provincial_tax=provincial_tax,
#         cpp_contribution=cpp_contribution,
#         total_tax_payable=total_tax_payable,
#         avg_tax_rate=avg_tax_rate,
#         marginal_tax_rate=marginal_tax_rate)
#     return result



# def estimate_ccpc_tax(revenue, deductions, tax_credits):
#     """
#     NOTE: re start-up costs: the first CAD 3,000 of incorporation expenses are deductible
#     """
#
#     taxable_revenue = calculate_ccpc_taxable_revenue(revenue, deductions)
#     federal_tax_rate = get_federal_corporate_tax(is_small_business=True)
#     provincial_tax_rate = get_provincial_corporate_tax(is_small_business=True)
#     net_federal_tax = taxable_revenue * federal_tax_rate
#     provincial_tax = taxable_revenue * provincial_tax_rate
#     tax_rate = federal_tax_rate + provincial_tax_rate
#
#     total_tax = taxable_revenue * tax_rate
#     total_tax_payable = calculate_ccpc_tax_reduction(total_tax, tax_credits)
#     avg_tax_rate = total_tax_payable / revenue
#     after_tax_revenue = revenue - total_tax_payable
#
#     corp_return = CorporateReturn(
#         revenue=revenue,
#         taxable_revenue=taxable_revenue,
#         after_tax_revenue=after_tax_revenue,
#         tax_credits=tax_credits,
#         deductions=deductions,
#         net_federal_tax=net_federal_tax,
#         provincial_tax=provincial_tax,
#         total_tax_payable=total_tax_payable,
#         avg_tax_rate=avg_tax_rate)
#
#     print("-" * 40)
#     print(f"CCPC Revenue")
#     print(f"  Revenue:\t\t\t${revenue:,.2f}")
#     print(f"Tax")
#     print(f"  Tax Payable: \t\t${total_tax_payable:,.2f}")
#     print(f"  Tax rate:\t\t\t  {tax_rate:,.2f}%")
#     print(f"  Avg Tax Rate: \t  {avg_tax_rate:,.2f}%")
#     print()
#     print(f"  After-tax revenue:\t${after_tax_revenue:,.2f}")
#     print("-" * 40)
#


# ------------------------------------------------------------------------------------------
def print_return_summary(result: IndividualReturn):
    print("-" * 40)
    print(f"Income & Deductions")
    print(f"  Employment income:\t${result.employment_income:,.2f}")
    print(f"  Total income:\t\t\t${result.total_income:,.2f}")
    print(f"  RRSP contribution: \t${result.rrsp_contribution:,.2f}")
    print()
    print(f"Taxable Income: \t\t${result.taxable_income:,.2f}")
    print("-" * 40)
    print(f"Taxes")
    print(f"  Federal Tax: \t\t\t${result.net_federal_tax:,.2f}")
    print(f"  Provincial Tax: \t\t${result.provincial_tax:,.2f}")
    print(f"  CPP Contributions: \t${result.cpp_contribution:,.2f}")
    print()
    print(f"Total Tax: \t\t\t\t${result.total_tax_payable:,.2f}")
    print("-" * 40)
    print()
    print(f"After-tax income: \t\t${result.after_tax_income:,.2f}")
    print(f"Average tax rate:\t\t{(result.avg_tax_rate * 100):,.2f}%")


# ------------------------------------------------------------------------------------------


def main(year, income, yearly_uccb, ei_benefits, investment_income,
         rrsp_contribution, medical_expenses, self_employed):
    """
    :param year: YYYY year. Must be one of {2023, 2024}
    :param income: employment income
    :param yearly_uccb: How much UCCB the Canadian government paid over the entire year
    :param ei_benefits: Employment Income benefits
    :param investment_income: Income from investments
    :param rrsp_contribution: RRSP contribution
    :param medical_expenses: Medical expenses
    :param verbose: Boolean - whether to print verbose results (True) or not (False)
    :return:
    """
    # # get Basic Personal Amount for a given year
    # bpa = get_bpa(year)
    # # compute CPP contribution for a given year
    # ympe = get_ympe(year)
    # cpp_rate = get_cpp_rate()
    # cpp_basic_annual_exemption = get_cpp_basic_annual_exemption()
    # cpp = calculate_cpp(ympe, income, cpp_basic_annual_exemption, cpp_rate, self_employed)
    # # Compute Canada employment amount
    # canada_employment_amount = get_canada_employment_amount(year, income)
    # # Get federal and provincial tax brackets
    # federal_tax_brackets = get_federal_tax_brackets(year)
    # provincial_tax_brackets = get_provincial_tax_brackets(year)
    #

    rev = IndividualRevenue(year)
    # tax_return = rev.compute_basic_return(income, yearly_uccb, ei_benefits, investment_income,
    #                                   rrsp_contribution, bpa, cpp, canada_employment_amount,
    #                                   medical_expenses, federal_tax_brackets,
    #                                   provincial_tax_brackets, verbose)

    tax_return = rev.compute_basic_return(income, yearly_uccb, ei_benefits, investment_income,
                                          rrsp_contribution, medical_expenses, self_employed)

    print_return_summary(tax_return)

def main2(revenue, deductions, tax_credits):
    rev = CorporateRevenue(year)
    rev.estimate_ccpc_tax(revenue, deductions, tax_credits)


if __name__ == "__main__":
    year = 2023
    income = 50000
    monthly_uccb = 217
    yearly_uccb = monthly_uccb * 12
    rrsp_contribution = 0.0
    ei_benefits = 0.0
    investment_income = 0.0
    medical_expenses = 0.0
    verbose = False
    self_employed = False
    main(year, income, yearly_uccb, ei_benefits, investment_income,
         rrsp_contribution, medical_expenses, self_employed)

    # ----------
    revenue = 50000
    deductions = 0
    tax_credits = 0
    # main2(revenue, deductions, tax_credits)