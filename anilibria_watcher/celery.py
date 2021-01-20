import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anilibria_watcher.settings')

celery_app = Celery('anilibria_watcher')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

celery_app.autodiscover_tasks()

celery_app.conf.beat_schedule = {
    'update-anime-db-every-three-minutes': {
        'task': 'watcher.tasks.background_update_anime',
        'schedule': crontab(),
    },
}
