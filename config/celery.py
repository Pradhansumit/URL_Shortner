import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.timezone = "Asia/Kolkata"

app.conf.beat_schedule = {
    "delete_old_urls": {
        "task": "api.tasks.delete_expired_urls",
        "schedule": crontab(minute=0, hour=0),  # Runs at midnight
    },
    # adds click count every 5 minutes to prevent performance issue
    "added_click_count": {
        "task": "api.tasks.update_click_counts",
        "schedule": crontab(minute="*/15"),  # runs every 25 minutes
    },
}


# @app.task(bind=True)
# def debug_task(self):
#     print(f"Request: {self.request!r}")
