from cra import CRA
from data_objects import CorporateReturn

"""
Note
- Most operating business expenses can be deducted from revenue earned for CCPC businesses
"""


class CorporateRevenue:

    def __init__(self, year):
        self.year = year
        self.cra = CRA(year)

    def estimate_ccpc_tax(self, revenue, cpp_contributions, deductions, tax_credits):
        """
        NOTE: re start-up costs: the first CAD 3,000 of incorporation expenses are deductible
        """

        taxable_revenue = self.calculate_ccpc_taxable_revenue(revenue, deductions)
        federal_tax_rate = self.cra.get_federal_corporate_tax(is_small_business=True)
        provincial_tax_rate = self.cra.get_provincial_corporate_tax(is_small_business=True)
        net_federal_tax = taxable_revenue * federal_tax_rate
        provincial_tax = taxable_revenue * provincial_tax_rate
        tax_rate = federal_tax_rate + provincial_tax_rate
        cpp_contribution = sum(cpp_contributions)

        total_tax = (taxable_revenue * tax_rate) + cpp_contribution
        total_tax_payable = self.calculate_ccpc_tax_reduction(total_tax, tax_credits)
        avg_tax_rate = total_tax_payable / revenue
        after_tax_revenue = revenue - total_tax_payable
        return CorporateReturn(
            revenue=revenue,
            taxable_revenue=taxable_revenue,
            after_tax_revenue=after_tax_revenue,
            tax_credits=tax_credits,
            deductions=deductions,
            tax_rate=tax_rate,
            net_federal_tax=net_federal_tax,
            provincial_tax=provincial_tax,
            cpp_contribution=cpp_contribution,
            total_tax_payable=total_tax_payable,
            avg_tax_rate=avg_tax_rate)

    def print_return_summary(self, tr: CorporateReturn):
        print("-" * 40)
        print(f"CCPC Revenue")
        print(f"  Revenue:\t\t\t${tr.revenue:,.2f}")
        print(f"Breakdown")
        print(f"  Net Federal:\t\t{tr.net_federal_tax:,.2f}")
        print(f"  Net Provincial:\t{tr.provincial_tax:,.2f}")
        print(f"  CPP Contribution:\t{tr.cpp_contribution:,.2f}")
        print(f"Tax")
        print(f"  Tax Payable: \t\t${tr.total_tax_payable:,.2f}")
        print(f"  Tax rate:\t\t\t  {tr.tax_rate:,.2f}%")
        print(f"  Avg Tax Rate: \t  {tr.avg_tax_rate:,.2f}%")
        print()
        print(f"  After-tax revenue:\t${tr.after_tax_revenue:,.2f}")
        print()
        print(f"deductions: {tr.deductions}")
        print("-" * 40)

        # ##########################################################################################
        # Estimate Corporate taxes
        # ##########################################################################################

    def calculate_ccpc_taxable_revenue(self, revenue, deductions):
        """
        TODO : figure out what ARE legitimate business deductions
        """
        return revenue - deductions

    def calculate_ccpc_tax_reduction(self, total_tax, tax_credits):
        """
        TODO : figure out what ARE legitimate business deductions
        """
        return total_tax - tax_credits
