from .celery_app import celery_app
from .utils import send_summary_to_all
import asyncio

@celery_app.task
def send_morning_summary():
    asyncio.run(send_summary_to_all())