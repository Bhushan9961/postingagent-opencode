import asyncio

from app.services.socialclaw_client import PROVIDER_MAP, SocialClawClient, SocialClawError
from app.workers.celery_app import celery_app


def _run_async(coro):
    return asyncio.run(coro)


@celery_app.task(bind=True, max_retries=3, default_retry_delay=120)
def publish_to_platform(
    self, content_id: int, platform: str, text: str, scheduled_at: str | None = None
) -> dict:
    try:
        client = SocialClawClient()
        provider = PROVIDER_MAP.get(platform, platform)
        schedule = {
            "posts": [
                {
                    "provider": provider,
                    "text": text,
                }
            ]
        }
        if scheduled_at:
            schedule["posts"][0]["scheduled_at"] = scheduled_at

        result = _run_async(client.apply_schedule(schedule))
        return {
            "content_id": content_id,
            "platform": platform,
            "status": "published",
            "result": result,
        }
    except SocialClawError as e:
        raise self.retry(exc=e, countdown=120)


@celery_app.task(bind=True, max_retries=2, default_retry_delay=60)
def check_publish_status(self, run_id: str) -> dict:
    try:
        client = SocialClawClient()
        return _run_async(client.get_run_status(run_id))
    except SocialClawError as e:
        raise self.retry(exc=e, countdown=60)
