import os
from celery import Celery

# Redis URL from environment or default
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "mediatrace",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["src.tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)
