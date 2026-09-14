from sqlalchemy import ForeignKey
from datetime import datetime
from typing import Any
from sqlalchemy import ForeignKey, JSON, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Source(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    adapter_id: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]
    authority_level: Mapped[int]
    url_template: Mapped[str | None]
    is_allowed: Mapped[bool] = mapped_column(default=True)
    rate_limit_per_sec: Mapped[float | None]
    capabilities: Mapped[Any | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    documents: Mapped[list["Document"]] = relationship(back_populates="source", cascade="all, delete-orphan")


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id"))
    company_id: Mapped[int | None] = mapped_column(ForeignKey("companies.id"))
    url: Mapped[str]
    content_hash: Mapped[str | None] = mapped_column(index=True)
    content_type: Mapped[str | None]
    retrieved_at: Mapped[datetime]
    http_status: Mapped[int | None]
    etag: Mapped[str | None]
    last_modified: Mapped[str | None]
    raw_content: Mapped[Any | None] = mapped_column(JSON)
    is_cached: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    source: Mapped["Source"] = relationship(back_populates="documents")
    company: Mapped["Company"] = relationship(back_populates="documents")
    evidence: Mapped[list["Evidence"]] = relationship(back_populates="document", cascade="all, delete-orphan")
