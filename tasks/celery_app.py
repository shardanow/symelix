from celery import Celery

celery_app = Celery(
    "tasks",
    include=[
        "tasks.reminders",
        "tasks.summary"
    ]
)


import tasks.scheduler