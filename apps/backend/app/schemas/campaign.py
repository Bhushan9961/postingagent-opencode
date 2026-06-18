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
    created_by: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CampaignUpdate(BaseModel):
    name: str | None = None
    goal: str | None = None
    target_audience: str | None = None
