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
    """Decorate a function for mongo connexion."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        response = f(s3, bucket *args, **kwargs)
        return response
    return wrapper


class S3:
    """S3 service."""
    @with_s3
    def get_object(s3, bucket, *args, **kwargs):
        """Get an object from S3."""
        return s3.get_object(bucket, *args, **kwargs)

    @with_s3
    def list_objects(s3, bucket, *args, **kwargs):
        """List objects from S3."""
        return s3.list_objects(bucket, *args, **kwargs)
    
    @with_s3
    def put_object(s3, bucket, *args, **kwargs):
        """Put an object to S3."""
        return s3.put_object(bucket, *args, **kwargs)
    