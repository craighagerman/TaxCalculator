from src.cra import CRA
from src.data_objects import CorporateReturn


class CorporateRevenue:

    def __init__(self, year):
        self.year = year
        self.cra = CRA(year)

    def estimate_ccpc_tax(self, revenue, deductions, tax_credits):
        """
        NOTE: re start-up costs: the first CAD 3,000 of incorporation expenses are deductible
        """

        taxable_revenue = self.calculate_ccpc_taxable_revenue(revenue, deductions)
        federal_tax_rate = self.cra.get_federal_corporate_tax(is_small_business=True)
        provincial_tax_rate = self.cra.get_provincial_corporate_tax(is_small_business=True)
        net_federal_tax = taxable_revenue * federal_tax_rate
        provincial_tax = taxable_revenue * provincial_tax_rate
        tax_rate = federal_tax_rate + provincial_tax_rate

        total_tax = taxable_revenue * tax_rate
        total_tax_payable = self.calculate_ccpc_tax_reduction(total_tax, tax_credits)
        avg_tax_rate = total_tax_payable / revenue
        after_tax_revenue = revenue - total_tax_payable

        corp_return = CorporateReturn(
            revenue=revenue,
            taxable_revenue=taxable_revenue,
            after_tax_revenue=after_tax_revenue,
            tax_credits=tax_credits,
            deductions=deductions,
            net_federal_tax=net_federal_tax,
            provincial_tax=provincial_tax,
            total_tax_payable=total_tax_payable,
            avg_tax_rate=avg_tax_rate)

        print("-" * 40)
        print(f"CCPC Revenue")
        print(f"  Revenue:\t\t\t${revenue:,.2f}")
        print(f"Tax")
        print(f"  Tax Payable: \t\t${total_tax_payable:,.2f}")
        print(f"  Tax rate:\t\t\t  {tax_rate:,.2f}%")
        print(f"  Avg Tax Rate: \t  {avg_tax_rate:,.2f}%")
        print()
        print(f"  After-tax revenue:\t${after_tax_revenue:,.2f}")
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

