from src.celery_app import celery_app
from src.main import run_pipeline
import logging

logger = logging.getLogger("MediaTrace.Tasks")

@celery_app.task(bind=True)
def analyze_video_task(self, url):
    logger.info(f"Starting async analysis for {url}")
    try:
        result = run_pipeline(url)
        return {"status": "completed", "result": result}
    except Exception as e:
        logger.error(f"Task failed: {e}")
        return {"status": "failed", "error": str(e)}
