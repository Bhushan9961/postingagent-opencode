import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.agents.graph import build_campaign_graph
from app.agents.state import CampaignState
from app.config.config import settings
from app.core.database import engine
from app.models.campaign import Campaign, CampaignStatus
from app.services.llm_client import get_llm_client
from app.services.social_publisher import SocialPublisher
from app.workers.celery_app import celery_app

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def _run_pipeline(campaign_id: int) -> dict:
    llm = get_llm_client()
    has_tokens = any([settings.linkedin_access_token, settings.facebook_page_access_token])
    publisher = SocialPublisher() if has_tokens else None
    graph = build_campaign_graph(llm, db_url=settings.database_url, publisher=publisher)

    async with SessionLocal() as session:
        result = await session.execute(select(Campaign).where(Campaign.id == campaign_id))
        campaign = result.scalar_one_or_none()
        if not campaign:
            return {"error": "Campaign not found"}
        campaign.status = CampaignStatus.RESEARCHING
        await session.commit()

        initial_state: CampaignState = {
            "campaign": {
                "name": campaign.name,
                "goal": campaign.goal,
                "target_audience": campaign.target_audience,
            },
            "research": {},
            "platform_rules": {},
            "strategy": {},
            "content_plan": {},
            "content_format": {},
            "story": {},
            "assets": {},
            "quality": {},
            "analytics": {},
            "learnings": {},
            "optimization": {},
        }

        try:
            final_state = await graph.ainvoke(initial_state)
            campaign.state_data = final_state
            campaign.status = CampaignStatus.COMPLETED
            campaign.research = final_state.get("research", {})
            campaign.strategy = final_state.get("strategy", {})
            campaign.content_plan = final_state.get("content_plan", {})
            campaign.analytics = final_state.get("analytics", {})
            campaign.learnings = final_state.get("learnings", {})
        except Exception as e:
            campaign.status = CampaignStatus.FAILED
            campaign.state_data = {"error": str(e)}
        await session.commit()
        return {"campaign_id": campaign_id, "status": campaign.status.value}


@celery_app.task(bind=True, max_retries=2, default_retry_delay=120)
def run_campaign_pipeline(self, campaign_id: int) -> dict:
    try:
        return asyncio.run(_run_pipeline(campaign_id))
    except Exception as e:
        raise self.retry(exc=e, countdown=120)
