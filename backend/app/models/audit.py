from sqlalchemy import ForeignKey
from datetime import datetime
from decimal import Decimal
from typing import Any
from sqlalchemy import ForeignKey, JSON, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.database import Base

class RetrievalRun(Base):
    __tablename__ = "retrieval_runs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    run_id: Mapped[str] = mapped_column(unique=True)
    company_id: Mapped[int | None] = mapped_column(ForeignKey("companies.id"))
    run_type: Mapped[str]
    started_at: Mapped[datetime]
    completed_at: Mapped[datetime | None]
    requests_made: Mapped[int] = mapped_column(default=0)
    cache_hits: Mapped[int] = mapped_column(default=0)
    facts_found: Mapped[int] = mapped_column(default=0)
    facts_rejected: Mapped[int] = mapped_column(default=0)
    facts_published: Mapped[int] = mapped_column(default=0)
    conflicts_detected: Mapped[int] = mapped_column(default=0)
    audit_failures: Mapped[int] = mapped_column(default=0)
    status: Mapped[str]
    error_message: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    company: Mapped["Company"] = relationship()
    audit_results: Mapped[list["AuditResult"]] = relationship(back_populates="run", cascade="all, delete-orphan")


class AuditResult(Base):
    __tablename__ = "audit_results"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    run_id: Mapped[str | None] = mapped_column(ForeignKey("retrieval_runs.run_id"))
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    fact_id: Mapped[int | None] = mapped_column(ForeignKey("company_facts.id"))
    audit_type: Mapped[str]
    publish_decision: Mapped[bool]
    risk_level: Mapped[str]
    reasons: Mapped[Any] = mapped_column(JSON)
    rejected_claims: Mapped[Any] = mapped_column(JSON)
    audited_at: Mapped[datetime]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    run: Mapped["RetrievalRun"] = relationship(back_populates="audit_results")
    company: Mapped["Company"] = relationship(back_populates="audit_results")
    fact: Mapped["CompanyFact"] = relationship()


class RefreshQueue(Base):
    __tablename__ = "refresh_queue"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), unique=True)
    priority: Mapped[int] = mapped_column(default=0)
    last_refreshed_at: Mapped[datetime | None]
    next_refresh_at: Mapped[datetime | None]
    refresh_reason: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    company: Mapped["Company"] = relationship(back_populates="refresh_queue")


class BudgetTracking(Base):
    __tablename__ = "budget_tracking"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    run_id: Mapped[str | None]
    source_adapter_id: Mapped[str | None]
    requests_used: Mapped[int] = mapped_column(default=0)
    requests_saved_by_cache: Mapped[int] = mapped_column(default=0)
    external_cost_estimate: Mapped[Decimal] = mapped_column(Numeric(precision=20, scale=2), default=0)
    timestamp: Mapped[datetime]
