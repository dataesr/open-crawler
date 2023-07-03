from celery import Celery

from open_crawler.config.config import settings


def create_celery_app():
    celery_app = Celery(settings.RABBITMQ_QUEUE_NAME, broker=settings.CELERY_BROKER_URL,
                        broker_connection_retry_on_startup=True)
    celery_app.config_from_object(settings, namespace='CELERY')
    celery_app.conf.update(task_track_started=True)
    celery_app.conf.update(task_serializer='pickle')
    celery_app.conf.update(result_serializer='pickle')
    celery_app.conf.update(accept_content=['pickle', 'json'])
    celery_app.conf.update(result_persistent=True)
    celery_app.conf.update(worker_send_task_events=False)
    celery_app.conf.update(worker_prefetch_multiplier=1)
    return celery_app

