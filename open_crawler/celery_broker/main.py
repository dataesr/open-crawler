from celery_broker.utils import create_celery_app

celery_app = create_celery_app()

if __name__ == "__main__":
    celery_app.start(
        argv=["-A", "main.celery_app", "worker", "-l", "info", "-P", "solo"]
    )
