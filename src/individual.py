from cra import CRA
from data_objects import IndividualReturn


class IndividualRevenue:

    def __init__(self, year):
        self.year = year
        self.cra = CRA(year)
        # get Basic Personal Amount for a given year
        self.bpa = self.cra.get_bpa()
        # compute CPP contribution for a given year
        self.ympe = self.cra.get_ympe()
        self.cpp_rate = self.cra.get_cpp_rate()
        self.cpp_basic_annual_exemption = self.cra.get_cpp_basic_annual_exemption()

    def compute_basic_return(self, employment_income, ucc_benefit, ei_benefits, investment_income,
                             rrsp_contribution, medical_expenses, self_employed):
        # compute CPP contribution
        cpp_contribution = self.calculate_cpp(employment_income, self_employed)
        # Compute Canada employment amount
        canada_employment_amount = self.cra.get_canada_employment_amount(employment_income)
        federal_tax_brackets = self.cra.get_federal_tax_brackets()
        provincial_tax_brackets = self.cra.get_provincial_tax_brackets()
        # ----------------------------------------------------------------------
        # Compute income
        total_income = self.calculate_total_income(employment_income, ucc_benefit, ei_benefits, investment_income)
        employment_deductions = self.calculate_employment_deductions(rrsp_contribution)
        taxable_income = self.calculate_net_income(total_income, employment_deductions)
        # TODO: compute cpp contribution here.
        # Compute taxes on taxable income
        basic_federal_tax = self.compute_federal_tax(taxable_income, federal_tax_brackets)
        provincial_tax = self.compute_provincial_tax(taxable_income, provincial_tax_brackets)
        marginal_tax_rate = self._compute_margin_tax_rate(taxable_income, federal_tax_brackets, provincial_tax_brackets)
        # Compute non-refundable tax credits
        # FIXME fix fed_non_refundable_tax_credit_rate
        tax_credits = self.compute_non_refundable_tax_credits(taxable_income, self.bpa, federal_tax_brackets,
                                                              cpp_contribution, canada_employment_amount,
                                                              ei_benefits, medical_expenses, taxable_income)
        # Compute net federal tax
        net_federal_tax = self.compute_net_federal_tax(basic_federal_tax, tax_credits)
        # Total tax payable
        total_tax_payable = net_federal_tax + provincial_tax
        after_tax_income = employment_income - total_tax_payable
        avg_tax_rate = total_tax_payable / employment_income
        return IndividualReturn(
            employment_income=employment_income,
            total_income=total_income,
            taxable_income=taxable_income,
            after_tax_income=after_tax_income,
            rrsp_contribution=rrsp_contribution,
            net_federal_tax=net_federal_tax,
            provincial_tax=provincial_tax,
            cpp_contribution=cpp_contribution,
            total_tax_payable=total_tax_payable,
            avg_tax_rate=avg_tax_rate,
            marginal_tax_rate=marginal_tax_rate)

    def print_return_summary(self, tr: IndividualReturn):
        print("-" * 40)
        print(f"Income & Deductions")
        print(f"  Employment income:\t${tr.employment_income:,.2f}")
        print(f"  Total income:\t\t\t${tr.total_income:,.2f}")
        print(f"  RRSP contribution: \t${tr.rrsp_contribution:,.2f}")
        print()
        print(f"Taxable Income: \t\t${tr.taxable_income:,.2f}")
        print(f"Taxes")
        print(f"  Federal Tax: \t\t\t${tr.net_federal_tax:,.2f}")
        print(f"  Provincial Tax: \t\t${tr.provincial_tax:,.2f}")
        print(f"  CPP Contributions: \t${tr.cpp_contribution:,.2f}")
        print()
        print(f"Total Tax: \t\t\t\t${tr.total_tax_payable:,.2f}")
        print()
        print(f"After-tax income: \t\t${tr.after_tax_income:,.2f}")
        print(f"Average tax rate:\t\t{(tr.avg_tax_rate * 100):,.2f}%")

    ############################################
    # Compute Basic Personal Amount
    ############################################
    def _compute_reduction_factor(self, bpa, brackets):
        threshold_bracket = brackets[3][0]
        top_bracket = brackets[4][0]
        additional_bpa = bpa.max - bpa.min
        return additional_bpa / (top_bracket - threshold_bracket)

    def _compute_additional_bpa(self, income, bpa, brackets):
        """
            When net income (line 23600) exceeds $173,205 in 2024,
            the $1,549 is reduced until income reaches $246,752 and the additional amount is zero.
            In other words, the additional amount is reduced by 2.1061%
        """
        threshold_bracket = brackets[3][0]
        default_additional_bpa = bpa.max - bpa.min
        if not income > threshold_bracket:
            return default_additional_bpa
        reduction_factor = self._compute_reduction_factor(bpa, brackets)
        return default_additional_bpa - (income - threshold_bracket) * reduction_factor

    def compute_bpa(self, income, bpa, brackets):
        add_bpa = self._compute_additional_bpa(income, bpa, brackets)
        return bpa.min + add_bpa

    ############################################
    # Calculate Employment Income
    ############################################
    def calculate_total_income(self, employment_income, ucc_benefit, ei_benefits, investment_income):
        return employment_income + ucc_benefit + ei_benefits + investment_income

    def calculate_employment_deductions(self, rrsp_contribution):
        return rrsp_contribution

    def calculate_net_income(self, total_income, employment_deductions):
        return total_income - employment_deductions

    ############################################
    # Calculate Canada Pension Plan (CPP) Contribution
    ############################################
    # def calculate_cpp(self, ympe, income, basic_deduction, cpp_rate, self_employed=False):
    #     """
    #     n.b. YMPE: Year's Maximum Pensionable Earnings. The earnings ceiling for CPP contributions
    #     """
    #     earnings = min(ympe, income)
    #     cpp = (earnings - basic_deduction) * cpp_rate
    #     cpp = cpp if not self_employed else cpp * 2
    #     return cpp

    def calculate_cpp(self, income, self_employed=False):
        """
        n.b. YMPE: Year's Maximum Pensionable Earnings. The earnings ceiling for CPP contributions
        """
        earnings = min(self.ympe, income)
        cpp = (earnings - self.cpp_basic_annual_exemption) * self.cpp_rate
        cpp = cpp if not self_employed else cpp * 2
        return cpp

    ############################################
    # Calculate Federal & Provincial Tax
    ############################################
    def _calculate_marginal_tax(self, amount, tax_rate):
        # print(f"bracket x rate:  {amount} x {tax_rate}")
        return amount * tax_rate

    def _get_taxable_amount(self, income, min_amount, max_amount):
        if min_amount < income <= max_amount:
            return income - min_amount
        elif income >= max_amount:
            return max_amount - min_amount
        elif income < min_amount:
            return 0
        else:
            return 0

    def _compute_bracket_taxes(self, income, brackets):
        def calculate_tax(item):
            marginal_amount = self._get_taxable_amount(income, item[0], item[1])
            # print(f"min: {item[0]}, income: {income}, max: {item[1]} ==> marginal_income: {marginal_income}")
            return self._calculate_marginal_tax(marginal_amount, item[2])

        taxes = [calculate_tax(item) for item in brackets]
        return taxes

    def compute_tax(self, income, brackets):
        return sum(self._compute_bracket_taxes(income, brackets))

    def compute_federal_tax(self, income, fed_brackets):
        # federal_tax_by_bracket = _compute_bracket_taxes(income, fed_brackets)
        # return sum(federal_tax_by_bracket)
        return self.compute_tax(income, fed_brackets)

    def compute_provincial_tax(self, income, provincial_brackets):
        # provincial_tax_by_bracket = _compute_bracket_taxes(income, provincial_brackets)
        # return sum(provincial_tax_by_bracket)
        return self.compute_tax(income, provincial_brackets)

    def get_marginal_tax_rate(self, income, brackets):
        for mn, mx, rate in brackets:
            if mn < income <= mx:
                return rate
        raise LookupError("Income not found in tax brackets")

    def _compute_margin_tax_rate(self, taxable_income, federal_brackets, provincial_brackets):
        fed_marginal_rate = self.get_marginal_tax_rate(taxable_income, federal_brackets)
        prov_marginal_rate = self.get_marginal_tax_rate(taxable_income, provincial_brackets)
        return fed_marginal_rate + prov_marginal_rate

    def compute_total_tax(self, federal_tax, provincial_tax, cpp_contribution, ei_contribution):
        return federal_tax + provincial_tax + cpp_contribution + ei_contribution

    def compute_simple_tax_return(self, income, fed_brackets, provincial_brackets, cpp_contribution, ei_contribution):
        federal_tax = self.compute_federal_tax(income, fed_brackets)
        provincial_tax = self.compute_provincial_tax(income, provincial_brackets)
        total_tax = self.compute_total_tax(federal_tax, provincial_tax, cpp_contribution, ei_contribution)
        net_income = income - total_tax

        print(f"Total Income:\t\t${income}")
        print("-" * 40)
        print(f"Federal tax:\t\t${federal_tax:,.2f}")
        print(f"Provincial tax:\t\t${provincial_tax:,.2f}")
        print(f"CPP contribution:\t${cpp_contribution:,.2f}")
        print(f"\tTotal tax:\t${total_tax:,.2f}")
        print("-" * 40)
        print(f"Net Income:\t\t${net_income:,.2f}")

    # compute_simple_tax_return(income, fed_2023, ont_2023, cpp_2023, ei_contribution)

    def compute_medical_expenses(self, medical_expenses, medical_expense_threshold):
        eligible_medical_expenses = medical_expenses - medical_expense_threshold
        return max(0.0, eligible_medical_expenses)

    #  Federal non-refundable tax credits
    def compute_non_refundable_tax_credits(self, income, bpa_range, federal_brackets, cpp_contribution,
                                           canada_employment_amount, ei_premiums,
                                           medical_expenses, net_income):
        bpa = self.compute_bpa(income, bpa_range, federal_brackets)
        income_tax_credit = net_income * 0.03  # line 108
        income_tax_credit = min(income_tax_credit, self.cra.basic_income_tax_credit)

        medical_expense_threshold = self.cra.get_medical_expense_threshold(income)
        eligible_medical_expenses = self.compute_medical_expenses(medical_expenses, medical_expense_threshold)
        tax_credits = sum([bpa, cpp_contribution, canada_employment_amount,
                           ei_premiums, income_tax_credit, eligible_medical_expenses])
        # Line 35000
        non_refundable_tax_credits = tax_credits * self.cra.fed_non_refundable_tax_credit_rate
        return non_refundable_tax_credits

    def compute_net_federal_tax(self, basic_federal_tax, non_refundable_tax_credits):
        return basic_federal_tax - non_refundable_tax_credits
