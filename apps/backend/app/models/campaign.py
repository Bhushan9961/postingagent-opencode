import enum
from datetime import datetime, timezone

from sqlalchemy import JSON, DateTime, Enum, Float, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class CampaignStatus(str, enum.Enum):
    DRAFT = "draft"
    RESEARCHING = "researching"
    PLANNING = "planning"
    CREATING_CONTENT = "creating_content"
    APPROVAL_PENDING = "approval_pending"
    APPROVED = "approved"
    PUBLISHING = "publishing"
    PUBLISHED = "published"
    ANALYZING = "analyzing"
    COMPLETED = "completed"
    FAILED = "failed"


class Campaign(Base):
    __tablename__ = "campaigns"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    client_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    goal: Mapped[str] = mapped_column(Text, nullable=True)
    target_audience: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[CampaignStatus] = mapped_column(
        Enum(CampaignStatus), default=CampaignStatus.DRAFT
    )
    state_data: Mapped[dict] = mapped_column(JSON, default=dict)
    research: Mapped[dict] = mapped_column(JSON, default=dict)
    strategy: Mapped[dict] = mapped_column(JSON, default=dict)
    content_plan: Mapped[dict] = mapped_column(JSON, default=dict)
    analytics: Mapped[dict] = mapped_column(JSON, default=dict)
    learnings: Mapped[dict] = mapped_column(JSON, default=dict)
    created_by: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
