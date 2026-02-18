from data_objects import BPA


class CRA:

    def __init__(self, year):
        self.year = year
        self.basic_income_tax_credit = 2635  # Line 109
        self.fed_non_refundable_tax_credit_rate = 0.15  # Line 114

    def get_federal_tax_brackets(self):
        match self.year:
            case year if year == 2024:
                return [(0, 55867, 0.15),
                        (55867, 111733, 0.205),
                        (111733, 173205, 0.26),
                        (173205, 246752, 0.29),
                        (246752, float('inf'), 0.33)]
            case year if year == 2023:
                return [(0, 53359, 0.15),
                        (53360, 106717, 0.205),
                        (106718, 165430, 0.26),
                        (165431, 235675, 0.29),
                        (235675, float('inf'), 0.33)]
            case _:
                raise ValueError("Invalid year. Must be one of {2023, 2024}")

    def get_provincial_tax_brackets(self):
        match self.year:
            case year if year == 2024:
                return [(0, 51446, 0.0505),
                        (51446, 102894, 0.0915),
                        (102894, 150000, 0.1116),
                        (150000, 220000, 0.1216),
                        (220000, float('inf'), 0.1316)]
            case year if year == 2023:
                return [(0, 49231, 0.0505),
                        (49231, 98463, 0.0915),
                        (98463, 150000, 0.1116),
                        (150000, 220000, 0.1216),
                        (220000, float('inf'), 0.1316)]
            case _:
                raise ValueError("Invalid year. Must be one of {2023, 2024}")


    def print_all_brackets(self):
        federal_tax_brackets = self.get_federal_tax_brackets()
        provincial_tax_brackets = self.get_provincial_tax_brackets()


    def get_federal_non_refundable_tax_credits_basic_personal_amount(self, net_income):
        """
        see: Line 30000 – Basic personal amount
        NOTE: I think this is just BPA!
        TODO: Refactor since it is computed elsewhere
        """
        if self.year == 2024:
            base_amount = 14156
            basic_supplemental_amount = 1549
            income_treshold = 173205.0
            if net_income >= 246752.0:
                return base_amount
            elif net_income <= income_treshold:
                return base_amount + basic_supplemental_amount
            else:
                adjusted_amount = (net_income - income_treshold) / 70245.00 * 1480.00
                supplemental_amount = max((basic_supplemental_amount - adjusted_amount), 0.0)
                return base_amount + supplemental_amount

        if self.year == 2023:
            base_amount = 13520.0
            basic_supplemental_amount = 1480.00
            income_treshold = 165430.0
            if net_income >= 235675:
                return base_amount
            elif net_income <= income_treshold:
                return base_amount + basic_supplemental_amount
            else:
                adjusted_amount = (net_income - income_treshold) / 70245.00 * 1480.00
                supplemental_amount = max((basic_supplemental_amount - adjusted_amount), 0.0)
                return base_amount + supplemental_amount
        raise ValueError("Invalid year. Must be one of {2023, 2024}")

    def get_canada_employment_amount(self, income):
        """

        The Canada employment amount is a non-refundable tax credit that you can
        claim if you reported employment income for the year. This amount is
        designed to help Canadians with some of their work-related expenses such
        as uniforms, home computers, and supplies needed to work.

        Note: Self-employed individuals cannot claim this amount.

        The amount you can claim is the lesser of:
        - the tax credit for a given year (e.g. For 2023 it was $1,368)
        - the total of the employment income that you reported on your return
        """
        match self.year:
            case year if year == 2024:
                return min(1433, income)
            case year if year == 2023:
                return min(1368, income)
            case _:
                raise ValueError("Invalid year. Must be one of {2023, 2024}")

    # Basic Personal Amount
    # Note: The "additional amount" is gradually reduced when net income (line 23600) is in excess of the bottom of the fourth tax bracket.
    # bpa_2024 = BPA(15705, 14156)
    # bpa_2023 = BPA(15000, 13521)
    def get_bpa(self):
        """
        n.b. The basic personal amount is the amount that can be earned before any
        federal/provincial/territorial tax is paid. Taxtips.ca lists it as a Tax Credit
        see: https://www.taxtips.ca/taxrates/calculating-canadian-personal-income-tax.htm
        From Fidelity:
        There are two sets of Basic Personal Amount that are applicable to Canadian taxpayers.
        The Federal Basic Personal Amount deducts Federal income tax for all taxpayers using the
        same thresholds across Canada. The provincial Basic Personal Amount is determined by
        each province with different thresholds and application rules.
        see: https://www.fidelity.ca/en/insights/articles/personal-amount-tax-credit-guide


        """
        match self.year:
            case year if year == 2024:
                return BPA(15705, 14156)
            case year if year == 2023:
                return BPA(15000, 13521)
            case _:
                raise ValueError("Invalid year. Must be one of {2023, 2024}")

    def get_ympe(self):
        match self.year:
            case year if year == 2024:
                return 68500
            case year if year == 2023:
                return 66600
            case _:
                raise ValueError("Invalid year. Must be one of {2023, 2024}")

    def get_medical_expense_threshold(self, income):
        pct = 0.03
        match self.year:
            case year if year == 2024:
                return min(2759, (income * pct))
            case year if year == 2023:
                return min(2635, (income * pct))
            case _:
                raise ValueError("Invalid year. Must be one of {2023, 2024}")

    # CPP (Canada Pension Plan) contributions
    # cpp_2024 = 3867.50
    # cpp_2023 = 3754.45

    def get_cpp_rate(self):
        return 0.0595

    def get_cpp_basic_annual_exemption(self):
        return 3500

    def max_cpp_pensionable_income(self):
        """
        Earnings up to the maximum pensionable income will be subject to CPP contributions
        """
        match self.year:
            case year if year == 2024:
                return 68500
            case year if year == 2023:
                return 66600
            case _:
                raise ValueError("Invalid year. Must be one of {2023, 2024}")


    def get_federal_corporate_tax(self, is_small_business=True):
        # n.b. year isn't relevant for 2023 vs 2024. May be in the future.
        if is_small_business:
            return 0.09
        return 0.15

    def get_provincial_corporate_tax(self, is_small_business=True):
        # n.b. year isn't relevant for 2023 vs 2024. May be in the future.
        if is_small_business:
            return 0.032
        return 0.115
