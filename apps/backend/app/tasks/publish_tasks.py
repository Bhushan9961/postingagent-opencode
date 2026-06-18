from app.services.social_publisher import SocialPublisher
from app.workers.celery_app import celery_app


def _run_async(coro):
    import asyncio
    return asyncio.run(coro)


@celery_app.task(bind=True, max_retries=3, default_retry_delay=120)
def publish_to_platform(
    self, platform: str, text: str, image_url: str | None = None
) -> dict:
    try:
        publisher = SocialPublisher()
        result = _run_async(publisher.publish(platform=platform, text=text, image_url=image_url))
        return {
            "platform": result.platform,
            "status": result.status,
            "post_id": result.post_id,
            "url": result.url,
            "error": result.error,
        }
    except Exception as e:
        raise self.retry(exc=e, countdown=120)
