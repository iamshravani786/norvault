from sqlalchemy import ForeignKey
from datetime import datetime, date
from decimal import Decimal
from typing import Any
from sqlalchemy import ForeignKey, JSON, Numeric, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.database import Base

class CompanyFact(Base):
    __tablename__ = "company_facts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    fact_type: Mapped[str] = mapped_column(index=True)
    subject: Mapped[str]
    predicate: Mapped[str]
    value_text: Mapped[str | None]
    value_numeric: Mapped[Decimal | None] = mapped_column(Numeric(precision=20, scale=2))
    value_json: Mapped[Any | None] = mapped_column(JSON)
    source_id: Mapped[int | None] = mapped_column(ForeignKey("sources.id"))
    document_id: Mapped[int | None] = mapped_column(ForeignKey("documents.id"))
    source_date: Mapped[date | None]
    retrieved_at: Mapped[datetime] = mapped_column(index=True)
    valid_from: Mapped[date | None]
    valid_to: Mapped[date | None]
    confidence: Mapped[float] = mapped_column(default=0.0)
    freshness_status: Mapped[str] = mapped_column(default="UNVERIFIED")
    identity_match_score: Mapped[float] = mapped_column(default=0.0)
    is_current: Mapped[bool] = mapped_column(default=True)
    fact_category: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    company: Mapped["Company"] = relationship(back_populates="facts")
    source: Mapped["Source"] = relationship()
    document: Mapped["Document"] = relationship()
    versions: Mapped[list["FactVersion"]] = relationship(back_populates="fact", cascade="all, delete-orphan")
    evidence: Mapped[list["Evidence"]] = relationship(back_populates="fact", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_company_facts_company_id_fact_type_is_current", "company_id", "fact_type", "is_current"),
    )


class FactVersion(Base):
    __tablename__ = "fact_versions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    fact_id: Mapped[int] = mapped_column(ForeignKey("company_facts.id"))
    version: Mapped[int]
    previous_value: Mapped[str | None]
    new_value: Mapped[str | None]
    changed_at: Mapped[datetime]
    change_source_id: Mapped[int | None] = mapped_column(ForeignKey("sources.id"))

    fact: Mapped["CompanyFact"] = relationship(back_populates="versions")
    change_source: Mapped["Source"] = relationship()


class Evidence(Base):
    __tablename__ = "evidence"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    fact_id: Mapped[int] = mapped_column(ForeignKey("company_facts.id"), index=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"))
    extraction_method: Mapped[str | None]
    extracted_value: Mapped[str | None]
    normalized_value: Mapped[str | None]
    identity_match_reasoning: Mapped[str | None]
    confidence: Mapped[float] = mapped_column(default=0.0)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    fact: Mapped["CompanyFact"] = relationship(back_populates="evidence")
    document: Mapped["Document"] = relationship(back_populates="evidence")
