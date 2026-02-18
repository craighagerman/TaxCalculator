from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Bracket:
    min: float
    max: float
    pct: float


@dataclass(frozen=True)
class BPA:
    max: float
    min: float
    addition: float = 0.0


@dataclass(frozen=True)
class Income:
    """
      uccb: Universal Child Care Benefit
      ei_benefits: Employment Income benefits
    """
    employment_income: float
    uccb: Optional[float] = None
    ei_benefits: Optional[float] = None
    investment_income: Optional[float] = None


@dataclass(frozen=True)
class IndividualReturn:
    employment_income: float
    total_income: float
    taxable_income: float
    after_tax_income: float
    rrsp_contribution: float
    net_federal_tax: float
    provincial_tax: float
    cpp_contribution: float
    total_tax_payable: float
    avg_tax_rate: float
    marginal_tax_rate: float


@dataclass(frozen=True)
class CorporateReturn:
    revenue: float
    taxable_revenue: float
    after_tax_revenue: float
    tax_credits: float
    deductions: float
    tax_rate: float
    net_federal_tax: float
    provincial_tax: float
    cpp_contribution: float
    total_tax_payable: float
    avg_tax_rate: float
