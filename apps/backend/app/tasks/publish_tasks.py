from app.workers.celery_app import celery_app


@celery_app.task(bind=True, max_retries=3, default_retry_delay=120)
def publish_to_platform(self, content_id: int, platform: str):
    return {"content_id": content_id, "platform": platform, "status": "pending"}
