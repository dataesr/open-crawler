from app.celery_broker.factory import create_celery_app

celery_app = create_celery_app()

if __name__ == "__main__":
    celery_app.start(
        argv=["-A", "celery_broker.main.celery_app", "worker", "-l", "info", "-P", "solo"]
    )
