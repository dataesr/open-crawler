import os
from functools import wraps
from minio import Minio

from app.config import settings

s3 = Minio(
    endpoint=settings.STORAGE_SERVICE_URL,
    access_key=settings.STORAGE_SERVICE_USERNAME,
    secret_key=settings.STORAGE_SERVICE_PASSWORD,
    secure=settings.STORAGE_SERVICE_SECURE,
    region=settings.STORAGE_SERVICE_REGION,
)

bucket = settings.STORAGE_SERVICE_BUCKET_NAME

if not s3.bucket_exists(bucket):
    s3.make_bucket(bucket)


def with_s3(f):
    """Decorate a function for s3 connexion."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        print(f"Calling {f.__name__} with s3 connexion", flush=True)
        print(f"args: {','.join(map(str,args))}", flush=True)
        response = f(s3, bucket, *args, **kwargs)
        return response
    return wrapper
