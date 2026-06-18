from datetime import datetime

from pydantic import BaseModel


class ContentCreate(BaseModel):
    campaign_id: int
    platform: str
    content_type: str
    caption: str | None = None


class ContentRead(BaseModel):
    id: int
    campaign_id: int
    platform: str
    content_type: str
    caption: str | None
    asset_urls: dict
    status: str
    brand_score: float
    quality_score: float
    is_rejected: bool
    publish_at: datetime | None
    published_at: datetime | None
    views: int
    likes: int
    shares: int
    created_at: datetime

    model_config = {"from_attributes": True}


class ContentUpdate(BaseModel):
    caption: str | None = None
    asset_urls: dict | None = None


class ContentApproval(BaseModel):
    approved: bool
    rejection_reason: str | None = None
