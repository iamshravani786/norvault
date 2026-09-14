from sqlalchemy import ForeignKey
from datetime import datetime, date
from decimal import Decimal
from typing import Any
from sqlalchemy import ForeignKey, JSON, Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.database import Base

class FinancialStatement(Base):
    __tablename__ = "financial_statements"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    fiscal_year: Mapped[int]
    statement_type: Mapped[str]
    currency: Mapped[str] = mapped_column(default="NOK")
    period_from: Mapped[date | None]
    period_to: Mapped[date | None]
    revenue: Mapped[Decimal | None] = mapped_column(Numeric(precision=20, scale=2))
    operating_profit: Mapped[Decimal | None] = mapped_column(Numeric(precision=20, scale=2))
    net_income: Mapped[Decimal | None] = mapped_column(Numeric(precision=20, scale=2))
    total_assets: Mapped[Decimal | None] = mapped_column(Numeric(precision=20, scale=2))
    equity: Mapped[Decimal | None] = mapped_column(Numeric(precision=20, scale=2))
    total_debt: Mapped[Decimal | None] = mapped_column(Numeric(precision=20, scale=2))
    current_assets: Mapped[Decimal | None] = mapped_column(Numeric(precision=20, scale=2))
    current_liabilities: Mapped[Decimal | None] = mapped_column(Numeric(precision=20, scale=2))
    long_term_debt: Mapped[Decimal | None] = mapped_column(Numeric(precision=20, scale=2))
    cash_and_equivalents: Mapped[Decimal | None] = mapped_column(Numeric(precision=20, scale=2))
    salary_costs: Mapped[Decimal | None] = mapped_column(Numeric(precision=20, scale=2))
    depreciation: Mapped[Decimal | None] = mapped_column(Numeric(precision=20, scale=2))
    financial_income: Mapped[Decimal | None] = mapped_column(Numeric(precision=20, scale=2))
    financial_expenses: Mapped[Decimal | None] = mapped_column(Numeric(precision=20, scale=2))
    tax_expense: Mapped[Decimal | None] = mapped_column(Numeric(precision=20, scale=2))
    ebt: Mapped[Decimal | None] = mapped_column(Numeric(precision=20, scale=2))
    raw_data: Mapped[Any | None] = mapped_column(JSON)
    source_id: Mapped[int | None] = mapped_column(ForeignKey("sources.id"))
    source_url: Mapped[str | None]
    retrieved_at: Mapped[datetime]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    company: Mapped["Company"] = relationship(back_populates="financial_statements")
    source: Mapped["Source"] = relationship()

    __table_args__ = (
        UniqueConstraint("company_id", "fiscal_year", "statement_type", name="uq_financial_statement"),
    )
