import asyncio
import nest_asyncio
from tasks.celery_app import celery_app
from tasks.utils import send_summary, get_active_users

# Loop for running async tasks in a synchronous context
# This is necessary for running async tasks in a synchronous context
# such as Celery tasks, which are typically run in a synchronous context.
# This is a workaround for the issue of running async tasks in a synchronous context
nest_asyncio.apply()

@celery_app.task
def send_morning_summary():
    print("📊 Задача send_morning_summary запущена")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_send_all())

async def _send_all():
    users = await get_active_users()
    for user in users:
        await send_summary(user.chat_id)
