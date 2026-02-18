# from src.corporate import calculate_ccpc_taxable_revenue, calculate_ccpc_tax_reduction, CorporateRevenue
from corporate import CorporateRevenue
from individual import IndividualRevenue


# ------------------------------------------------------------------------------------------

def run_main():
    year = 2024
    # monthly_uccb_income = 0
    # monthly_uccb_income = 217  # money from Can gov for children
    monthly_uccb_income = 201.18   # n.b. actual average monthly paid in 2024
    ei_benefits = 0.0           # money from Can gov for unemployment
    investment_income = 0.0     # income from investments (assume 0)
    medical_expenses = 0.0      # assume 0 for now (we will have eliglble deductions)
    self_employed = False
    # jobscan_revenue = 215000   # n.b. this is annual
    jobscan_revenue = 158764.96  # n.b. this is actual for 2024

    num_months = 8.5 # n.b. this is the actual number of months for corporation in 2024

    # adjust parameters below to see different results
    # craig_income = 100000
    # miki_income = 50000
    # craig_income = 93186.96
    # miki_income = 42421.44

    # craig_annual_gross_income = 100000
    # craig_monthly_gross_income = craig_annual_gross_income / 12
    # craig_income = craig_monthly_gross_income * num_months  # 66,666.667
    # craig_income = 62088  # actual paid out
    craig_income = 70833.33 # actual gross

    # craig_income = 100000

    # miki_annual_gross_income = 50000
    # miki_monthly_gross_income = miki_annual_gross_income / 12
    # miki_income = miki_monthly_gross_income * num_months  # 33,333.333
    # miki_income = 27745.84  # actual paid out
    miki_income = 35416.67  # actual gross

    # miki_income = 50000


    # craig_rrsp = 50000
    craig_rrsp = 34000  # 50k annual amortized at 8 months
    # craig_rrsp = 0
    miki_rrsp = 0

    main(year, monthly_uccb_income, ei_benefits, investment_income, medical_expenses, jobscan_revenue,
         miki_income, craig_income, miki_rrsp, craig_rrsp, self_employed)



def main(year, monthly_uccb_income, ei_benefits, investment_income, medical_expenses, jobscan_revenue,
         miki_income, craig_income, miki_rrsp, craig_rrsp, self_employed):
    yearly_uccb_income = monthly_uccb_income * 12
    incomes = [miki_income, craig_income]
    print("\nINDIVIDUAL")
    # print("-" * 40)
    # print("CRAIG (as a sole proprietor)")
    # craig = main_individual(year, 215000, yearly_uccb, ei_benefits, investment_income,
    #                 craig_rrsp, medical_expenses, self_employed)
    # print("\n***\n")

    print("-" * 40)
    print("CRAIG")
    craig = main_individual(year, incomes[1], 0, ei_benefits, investment_income,
                    craig_rrsp, medical_expenses, self_employed)
    print("-"*40)
    print("MIKI")
    miki = main_individual(year, incomes[0], yearly_uccb_income, ei_benefits, investment_income,
                    miki_rrsp, medical_expenses, self_employed)

    # ----------
    # CORPORATE RETURNS
    print("-" * 40)
    print("CORPORATE")
    sum_incomes = sum(incomes)
    revenue = jobscan_revenue - sum(incomes)
    cpp_contributions = [craig.cpp_contribution, miki.cpp_contribution]
    deductions = 0
    tax_credits = 0
    corp = main_corporate(year, revenue, cpp_contributions, deductions, tax_credits)

    mc_earnings = craig.after_tax_income + miki.after_tax_income
    total_earnings = craig.after_tax_income + miki.after_tax_income + corp.after_tax_revenue
    total_rrsp = craig_rrsp + miki_rrsp
    total_tax = craig.total_tax_payable + miki.total_tax_payable + corp.total_tax_payable

    print("\n\n-----     SUMMARY     -----")
    print(f"Net Income (Miki + Craig Take-home):\t${mc_earnings:,.2f}")
    print(f"\tNet Monthly Income (M + C):\t\t\t${(mc_earnings / 12):,.2f}")
    print(f"Total Net Income (Miki, Craig, Corp): \t${total_earnings:,.2f}")
    print(f"Total RRSP Contribution (C+M): \t\t\t${total_rrsp:,.2f}")
    print(f"Total Tax owned (personal+corp): \t\t${total_tax:,.2f}" )
    print("-"*40)
    print("\n\n-----     MONTHLY     -----")
    craig_net_monthly = craig.after_tax_income / 12
    miki_net_monthly = miki.after_tax_income / 12
    tax_monthly = total_tax / 12
    total_rrsp_monthly = total_rrsp / 12
    monthly_subtotal = craig_net_monthly + miki_net_monthly + tax_monthly + total_rrsp_monthly
    print(f"Net Income Craig:\t${craig_net_monthly:,.2f}")
    print(f"Net Income Miki:\t${miki_net_monthly:,.2f}")
    print(f"Total Tax Owed:\t\t${tax_monthly:,.2f}")
    print(f"RRSP Contribution:\t${total_rrsp_monthly:,.2f}")
    print(f"\tTOTAL DISBURSEMENT:\t${monthly_subtotal:,.2f}")
    print()
    mrr = 18000 # i.e. estimate of current/max MRR (monthly recurring revenue)
    print(f"\tMRR Threshold: \t\t${mrr:,.2f}")
    left_over = mrr - monthly_subtotal
    print(f"\tMRR - Disbursement: ${left_over:,.2f}")
    print()
    print(f"payments-c{int(craig_income*0.001)}_m{int(miki_income*0.001)}_rrsp{int(total_rrsp*0.001)}")





def main_individual(year, income, yearly_uccb, ei_benefits, investment_income,
         rrsp_contribution, medical_expenses, self_employed):
    rev = IndividualRevenue(year)
    tax_return = rev.compute_basic_return(income, yearly_uccb, ei_benefits, investment_income,
                                          rrsp_contribution, medical_expenses, self_employed)
    rev.print_return_summary(tax_return)
    return tax_return


def main_corporate(year, revenue, cpp_contributions, deductions, tax_credits):
    rev = CorporateRevenue(year)
    tax_return = rev.estimate_ccpc_tax(revenue, cpp_contributions, deductions, tax_credits)
    rev.print_return_summary(tax_return)
    return tax_return


if __name__ == "__main__":
    run_main()
