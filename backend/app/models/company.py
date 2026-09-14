from sqlalchemy import ForeignKey
from datetime import datetime, date
from typing import Any
from sqlalchemy import ForeignKey, JSON, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.database import Base

class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    org_number: Mapped[str] = mapped_column(unique=True, index=True)
    name: Mapped[str]
    org_form_code: Mapped[str | None]
    org_form_description: Mapped[str | None]
    status: Mapped[str] = mapped_column(default="active")
    registration_date: Mapped[date | None]
    foundation_date: Mapped[date | None]
    deletion_date: Mapped[date | None]
    bankruptcy: Mapped[bool] = mapped_column(default=False)
    under_liquidation: Mapped[bool] = mapped_column(default=False)
    forced_liquidation: Mapped[bool] = mapped_column(default=False)
    registered_in_vat: Mapped[bool | None]
    registered_in_business_register: Mapped[bool | None]
    registered_in_foundation_register: Mapped[bool | None]
    registered_in_nonprofit_register: Mapped[bool | None]
    latest_annual_accounts_year: Mapped[int | None]
    institutional_sector_code: Mapped[str | None]
    institutional_sector_desc: Mapped[str | None]
    language_form: Mapped[str | None]
    homepage: Mapped[str | None]
    email: Mapped[str | None]
    phone: Mapped[str | None]
    profile_status: Mapped[str] = mapped_column(default="seeded")
    identity_confidence: Mapped[float | None]
    last_verified_at: Mapped[datetime | None]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    aliases: Mapped[list["CompanyAlias"]] = relationship(back_populates="company", cascade="all, delete-orphan")
    addresses: Mapped[list["CompanyAddress"]] = relationship(back_populates="company", cascade="all, delete-orphan")
    roles: Mapped[list["CompanyRole"]] = relationship(back_populates="company", cascade="all, delete-orphan")
    industries: Mapped[list["CompanyIndustry"]] = relationship(back_populates="company", cascade="all, delete-orphan")
    facts: Mapped[list["CompanyFact"]] = relationship(back_populates="company", cascade="all, delete-orphan")
    events: Mapped[list["CompanyEvent"]] = relationship(back_populates="company", cascade="all, delete-orphan")
    financial_statements: Mapped[list["FinancialStatement"]] = relationship(back_populates="company", cascade="all, delete-orphan")
    conflicts: Mapped[list["Conflict"]] = relationship(back_populates="company", cascade="all, delete-orphan")
    relationships_as_parent: Mapped[list["CorporateRelationship"]] = relationship(
        foreign_keys="[CorporateRelationship.parent_company_id]",
        back_populates="parent_company",
        cascade="all, delete-orphan"
    )
    relationships_as_child: Mapped[list["CorporateRelationship"]] = relationship(
        foreign_keys="[CorporateRelationship.child_company_id]",
        back_populates="child_company",
        cascade="all, delete-orphan"
    )
    documents: Mapped[list["Document"]] = relationship(back_populates="company", cascade="all, delete-orphan")
    audit_results: Mapped[list["AuditResult"]] = relationship(back_populates="company", cascade="all, delete-orphan")
    refresh_queue: Mapped["RefreshQueue"] = relationship(back_populates="company", uselist=False, cascade="all, delete-orphan")


    def __repr__(self) -> str:
        return f"<Company(org_number='{self.org_number}', name='{self.name}')>"


class CompanyAlias(Base):
    __tablename__ = "company_aliases"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    name: Mapped[str]
    name_type: Mapped[str]
    valid_from: Mapped[date | None]
    valid_to: Mapped[date | None]
    source_id: Mapped[int | None] = mapped_column(ForeignKey("sources.id"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    company: Mapped["Company"] = relationship(back_populates="aliases")
    source: Mapped["Source"] = relationship()


class CompanyAddress(Base):
    __tablename__ = "company_addresses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    address_type: Mapped[str]
    street_lines: Mapped[Any | None] = mapped_column(JSON)
    postal_code: Mapped[str | None]
    city: Mapped[str | None]
    municipality_code: Mapped[str | None]
    municipality_name: Mapped[str | None]
    country_code: Mapped[str] = mapped_column(default="NO")
    country_name: Mapped[str] = mapped_column(default="Norge")
    valid_from: Mapped[date | None]
    valid_to: Mapped[date | None]
    is_current: Mapped[bool] = mapped_column(default=True)
    source_id: Mapped[int | None] = mapped_column(ForeignKey("sources.id"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    company: Mapped["Company"] = relationship(back_populates="addresses")
    source: Mapped["Source"] = relationship()


class CompanyRole(Base):
    __tablename__ = "company_roles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    role_group_code: Mapped[str | None]
    role_group_description: Mapped[str | None]
    role_type_code: Mapped[str]
    role_type_description: Mapped[str | None]
    person_first_name: Mapped[str | None]
    person_last_name: Mapped[str | None]
    person_middle_name: Mapped[str | None]
    person_birth_date: Mapped[date | None]
    is_deceased: Mapped[bool] = mapped_column(default=False)
    is_resigned: Mapped[bool] = mapped_column(default=False)
    entity_org_number: Mapped[str | None]
    entity_name: Mapped[str | None]
    last_changed: Mapped[date | None]
    source_id: Mapped[int | None] = mapped_column(ForeignKey("sources.id"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    company: Mapped["Company"] = relationship(back_populates="roles")
    source: Mapped["Source"] = relationship()


class CompanyIndustry(Base):
    __tablename__ = "company_industries"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    priority: Mapped[int]
    nace_code: Mapped[str]
    nace_description: Mapped[str | None]
    source_id: Mapped[int | None] = mapped_column(ForeignKey("sources.id"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    company: Mapped["Company"] = relationship(back_populates="industries")
    source: Mapped["Source"] = relationship()


class CorporateRelationship(Base):
    __tablename__ = "corporate_relationships"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    parent_company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    child_company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    relationship_type: Mapped[str]
    source_id: Mapped[int | None] = mapped_column(ForeignKey("sources.id"))
    valid_from: Mapped[date | None]
    valid_to: Mapped[date | None]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    parent_company: Mapped["Company"] = relationship(foreign_keys=[parent_company_id], back_populates="relationships_as_parent")
    child_company: Mapped["Company"] = relationship(foreign_keys=[child_company_id], back_populates="relationships_as_child")
    source: Mapped["Source"] = relationship()


class CompanyEvent(Base):
    __tablename__ = "company_events"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    event_type: Mapped[str]
    event_date: Mapped[date | None]
    description: Mapped[str | None]
    old_value: Mapped[str | None]
    new_value: Mapped[str | None]
    source_id: Mapped[int | None] = mapped_column(ForeignKey("sources.id"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    company: Mapped["Company"] = relationship(back_populates="events")
    source: Mapped["Source"] = relationship()

    __table_args__ = (
        Index("ix_company_events_company_id_event_date", "company_id", "event_date"),
    )
