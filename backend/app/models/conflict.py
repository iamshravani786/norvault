from sqlalchemy import ForeignKey
from datetime import datetime
from typing import Any
from sqlalchemy import ForeignKey, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.database import Base

class Conflict(Base):
    __tablename__ = "conflicts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    fact_type: Mapped[str]
    values: Mapped[Any] = mapped_column(JSON)
    sources_involved: Mapped[Any] = mapped_column(JSON)
    temporal_context: Mapped[str | None]
    identity_context: Mapped[str | None]
    resolution: Mapped[str | None]
    resolution_reasoning: Mapped[str | None]
    resolved_at: Mapped[datetime | None]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    company: Mapped["Company"] = relationship(back_populates="conflicts")
