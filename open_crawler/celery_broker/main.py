from open_crawler.celery_broker.tasks import celery_app

if __name__ == "__main__":
    celery_app.start(argv=['-A', 'main.celery_app', 'worker', '-l', 'debug'])