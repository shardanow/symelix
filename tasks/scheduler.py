from celery.schedules import crontab
from tasks.celery_app import celery_app

celery_app.conf.beat_schedule = {
    # "send_morning_summary": {
    #     "task": "tasks.summary.send_morning_summary",
    #     "schedule": crontab(hour=10, minute=0),
    # },
    "remind_hydrate": {
        "task": "tasks.reminders.remind_hydrate",
        "schedule": crontab(hour='10,12,14,16,18,20', minute=0)
    },
    "remind_vitamins": {
        "task": "tasks.reminders.remind_vitamins",
        "schedule": crontab(hour=11, minute=0)
    },
    "remind_exercise": {
        "task": "tasks.reminders.remind_exercise",
        "schedule": crontab(minute=30)
    }
}
