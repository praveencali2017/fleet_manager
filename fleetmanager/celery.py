import os
from celery import Celery
from loguru import logger
from celery.schedules import crontab
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fleetmanager.settings')

app = Celery('fleetmanager')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

logger.info(f"Cron job interval set: {settings.CHECK_TASK_CRON_INTERVAL}")
app.conf.beat_schedule = {
    'task-manager-check': {
        'task': 'task_management.tasks.check_tasks',
        'schedule': crontab(minute=settings.CHECK_TASK_CRON_INTERVAL),
    },
}