from app.factory import create_api_app, create_celery_app

api_app = create_api_app()
celery_app = create_celery_app()
