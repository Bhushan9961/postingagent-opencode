from datetime import datetime
from pydantic import BaseModel


class CampaignStateData(BaseModel):
    campaign: dict = {}
    research: dict = {}
    platform_rules: dict = {}
    strategy: dict = {}
    content_plan: dict = {}
    content_format: dict = {}
    story: dict = {}
    assets: dict = {}
    quality: dict = {}
    analytics: dict = {}
    learnings: dict = {}
    optimization: dict = {}


class ResearchData(BaseModel):
    competitors: list[dict] = []
    pain_points: list[str] = []
    trends: list[str] = []
    customer_desires: list[str] = []
    reddit_insights: list[str] = []


class StrategyData(BaseModel):
    theme: str = ""
    positioning: str = ""
    core_emotion: str = ""
    marketing_angle: str = ""
    offer_strategy: str = ""


class ContentPlanItem(BaseModel):
    day: int
    platform: str
    content_type: str
    title: str
    description: str
    cta: str = ""


class ContentPlan(BaseModel):
    items: list[ContentPlanItem] = []


class StoryData(BaseModel):
    hook: str = ""
    script: str = ""
    narrative: str = ""
    cta: str = ""
    scenes: list[dict] = []
