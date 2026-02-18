import json
from pathlib import Path

from data_objects import BPA


def _load_cra_config():
    """Load CRA parameters from data/cra_config.json (keyed by tax year)."""
    config_path = Path(__file__).resolve().parent.parent / "data" / "cra_config.json"
    with open(config_path, encoding="utf-8") as f:
        return json.load(f)


def _brackets_from_config(bracket_list):
    """Convert config bracket list (null = infinity) to list of (min, max, rate) tuples."""
    result = []
    for min_val, max_val, rate in bracket_list:
        max_val = float("inf") if max_val is None else max_val
        result.append((min_val, max_val, rate))
    return result


class CRA:

    def __init__(self, year):
        self.year = year
        config = _load_cra_config()
        year_str = str(year)
        if year_str not in config:
            supported = ", ".join(sorted(config.keys()))
            raise ValueError(f"Invalid year. Must be one of {{{supported}}}")
        self._config = config[year_str]
        self.basic_income_tax_credit = self._config["basic_income_tax_credit"]
        self.fed_non_refundable_tax_credit_rate = self._config["fed_non_refundable_tax_credit_rate"]

    def get_federal_tax_brackets(self):
        return _brackets_from_config(self._config["federal_tax_brackets"])

    def get_provincial_tax_brackets(self):
        return _brackets_from_config(self._config["provincial_tax_brackets"])

    def print_all_brackets(self):
        federal_tax_brackets = self.get_federal_tax_brackets()
        provincial_tax_brackets = self.get_provincial_tax_brackets()

    def get_federal_non_refundable_tax_credits_basic_personal_amount(self, net_income):
        """
        see: Line 30000 – Basic personal amount
        NOTE: I think this is just BPA!
        TODO: Refactor since it is computed elsewhere
        """
        c = self._config["basic_personal_amount_credit"]
        base_amount = c["base_amount"]
        basic_supplemental_amount = c["basic_supplemental_amount"]
        income_threshold = c["income_threshold"]
        max_income_full_reduction = c["max_income_full_reduction"]
        phase_out_range = c["phase_out_range"]
        phase_out_reduction_amount = c["phase_out_reduction_amount"]

        if net_income >= max_income_full_reduction:
            return base_amount
        if net_income <= income_threshold:
            return base_amount + basic_supplemental_amount
        adjusted_amount = (net_income - income_threshold) / phase_out_range * phase_out_reduction_amount
        supplemental_amount = max((basic_supplemental_amount - adjusted_amount), 0.0)
        return base_amount + supplemental_amount

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
        max_amount = self._config["canada_employment_amount_max"]
        return min(max_amount, income)

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
        bpa = self._config["bpa"]
        return BPA(bpa["max"], bpa["min"])

    def get_provincial_bpa(self):
        """
        Provincial basic personal amount (Ontario in current config).
        Used as a non-refundable tax credit at the province's lowest bracket rate.
        """
        return self._config["provincial_bpa"]

    def get_ympe(self):
        return self._config["ympe"]

    def get_medical_expense_threshold(self, income):
        m = self._config["medical_expense_threshold"]
        return min(m["floor"], income * m["pct_of_income"])

    def get_cpp_rate(self):
        return self._config["cpp"]["rate"]

    def get_cpp_basic_annual_exemption(self):
        return self._config["cpp"]["basic_annual_exemption"]

    def max_cpp_pensionable_income(self):
        """
        Earnings up to the maximum pensionable income will be subject to CPP contributions
        """
        return self._config["cpp"]["max_pensionable_income"]

    def get_federal_corporate_tax(self, is_small_business=True):
        corp = self._config["corporate_tax"]["federal"]
        return corp["small_business"] if is_small_business else corp["general"]

    def get_provincial_corporate_tax(self, is_small_business=True):
        corp = self._config["corporate_tax"]["provincial"]
        return corp["small_business"] if is_small_business else corp["general"]
