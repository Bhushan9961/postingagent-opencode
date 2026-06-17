from app.workers.celery_app import celery_app


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def run_campaign_pipeline(self, campaign_id: int):
    return {"campaign_id": campaign_id, "status": "started"}
