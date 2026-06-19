from datetime import datetime

from pydantic import BaseModel


class CampaignCreate(BaseModel):
    name: str
    goal: str | None = None
    target_audience: str | None = None


class CampaignRead(BaseModel):
    id: int
    name: str
    goal: str | None
    target_audience: str | None
    status: str
    state_data: dict | None = None
    research: dict | None = None
    strategy: dict | None = None
    content_plan: dict | None = None
    analytics: dict | None = None
    learnings: dict | None = None
    created_by: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CampaignUpdate(BaseModel):
    name: str | None = None
    goal: str | None = None
    target_audience: str | None = None
