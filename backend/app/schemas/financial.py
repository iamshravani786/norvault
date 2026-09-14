from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict

class BrregDriftsinntekter(BaseModel):
    salgsinntekter: Decimal | None = None
    annenDriftsinntekt: Decimal | None = None
    sumDriftsinntekter: Decimal | None = None

class BrregDriftskostnader(BaseModel):
    varekostnad: Decimal | None = None
    lonnskostnad: Decimal | None = None
    avskrivningPaaVarigeDriftsmidlerOgImmaterielleEiendeler: Decimal | None = None
    annenDriftskostnad: Decimal | None = None
    sumDriftskostnader: Decimal | None = None

class BrregDriftsresultat(BaseModel):
    driftsinntekter: BrregDriftsinntekter | None = None
    driftskostnader: BrregDriftskostnader | None = None
    driftsresultat: Decimal | None = None

class BrregFinansinntekter(BaseModel):
    sumFinansinntekter: Decimal | None = None
    renteinntektFraForetakISammeKonsern: Decimal | None = None
    annenRenteinntekt: Decimal | None = None
    annenFinansinntekt: Decimal | None = None

class BrregFinanskostnader(BaseModel):
    sumFinanskostnader: Decimal | None = None
    rentekostnadTilForetakISammeKonsern: Decimal | None = None
    annenRentekostnad: Decimal | None = None
    annenFinanskostnad: Decimal | None = None

class BrregFinansresultat(BaseModel):
    finansinntekter: BrregFinansinntekter | None = None
    finanskostnader: BrregFinanskostnader | None = None
    nettoFinans: Decimal | None = None

class BrregResultatregnskap(BaseModel):
    driftsresultat: BrregDriftsresultat | None = None
    finansresultat: BrregFinansresultat | None = None
    ordinaertResultatFoerSkattekostnad: Decimal | None = None
    skattekostnadPaaOrdinaertResultat: Decimal | None = None
    aarsresultat: Decimal | None = None

class BrregAnleggsmidler(BaseModel):
    sumAnleggsmidler: Decimal | None = None

class BrregOmloepsmidler(BaseModel):
    sumOmloepsmidler: Decimal | None = None
    kassabeholdning: Decimal | None = None

class BrregEiendeler(BaseModel):
    anleggsmidler: BrregAnleggsmidler | None = None
    omloepsmidler: BrregOmloepsmidler | None = None
    sumEiendeler: Decimal | None = None

class BrregEgenkapital(BaseModel):
    sumEgenkapital: Decimal | None = None
    opptjentEgenkapital: dict | None = None
    innskuttEgenkapital: dict | None = None

class BrregGjeld(BaseModel):
    sumGjeld: Decimal | None = None
    kortsiktigGjeld: dict | None = None
    langsiktigGjeld: dict | None = None

class BrregEgenkapitalGjeld(BaseModel):
    egenkapital: BrregEgenkapital | None = None
    gjeld: BrregGjeld | None = None
    sumEgenkapitalOgGjeld: Decimal | None = None

class BrregRegnskapResponse(BaseModel):
    """A single annual account record from Brreg."""
    journalnr: str | None = None
    regnskapsperiode: dict | None = None  # {fraDato, tilDato}
    valuta: str | None = None
    avviklingsregnskap: bool | None = None
    oppstillingsplan: str | None = None  # 'store' or 'sma'
    revisjonsberetning: str | None = None
    regnskapstype: str | None = None  # 'SELSKAP' or 'KONSERN'
    resultatregnskap: BrregResultatregnskap | None = None
    eiendeler: BrregEiendeler | None = None
    egenkapitalGjeld: BrregEgenkapitalGjeld | None = None

class FinancialStatementRead(BaseModel):
    """Normalized financial statement for API response."""
    model_config = ConfigDict(from_attributes=True)
    fiscal_year: int
    statement_type: str
    currency: str = 'NOK'
    revenue: Decimal | None = None
    operating_profit: Decimal | None = None
    net_income: Decimal | None = None
    total_assets: Decimal | None = None
    equity: Decimal | None = None
    total_debt: Decimal | None = None
    cash_and_equivalents: Decimal | None = None
    salary_costs: Decimal | None = None
    source_name: str
    source_url: str
    retrieved_at: datetime
    confidence: float
    freshness_status: str

class FinancialSummary(BaseModel):
    """Multi-year financial summary."""
    statements: list[FinancialStatementRead]
    latest_year: int | None = None
    has_group_accounts: bool = False
