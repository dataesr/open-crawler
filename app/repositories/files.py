import io
import json
from zipfile import ZipFile, ZIP_DEFLATED
from app.services.s3 import with_s3
from app.config import settings


HTML_FOLDER_NAME = settings.HTML_FOLDER_NAME.strip('/')
METADATA_FOLDER_NAME = settings.METADATA_FOLDER_NAME.strip('/')


class FileRepository:
    """Operations for crawls collection"""

    @staticmethod
    @with_s3
    def delete_all_crawl_files(s3, bucket, crawl_id):
        """Delete all crawl's files from the storage service"""
        objects = s3.list_objects(bucket, prefix=crawl_id, recursive=True)
        for obj in objects:
            s3.remove_object(bucket, obj.object_name)
        return

    @staticmethod
    @with_s3
    def store_metadata_file(s3, bucket, crawl_id, key, data):
        """Store a crawl file in the storage service"""
        _key = f"{crawl_id}/{METADATA_FOLDER_NAME}/{key}"
        _bytes = data.encode('utf-8')
        _data = io.BytesIO(_bytes)
        return s3.put_object(bucket, object_name=_key, length=len(_bytes), content_type="application/json", data=_data)

    @staticmethod
    @with_s3
    def store_html_file(s3, bucket, crawl_id, key, data):
        """Store a crawl file in the storage service"""
        _key = f"{crawl_id}/{HTML_FOLDER_NAME}/{key}"
        _bytes = data.encode('utf-8')
        _data = io.BytesIO(_bytes)
        return s3.put_object(bucket, object_name=_key, length=len(_bytes), content_type='text/html', data=_data)

    @staticmethod
    @with_s3
    def zip_all_crawl_files(s3, bucket, crawl_id) -> ZipFile:
        """Zip all crawl's files from the storage service"""
        zip_io = io.BytesIO()
        objects = s3.list_objects(bucket, prefix=crawl_id, recursive=True)
        with ZipFile(zip_io, "a", ZIP_DEFLATED, False) as zipper:
            for obj in objects:
                file = s3.get_object(bucket, obj.object_name).read()
                zipper.writestr(obj.object_name.strip(crawl_id), file)
        return zip_io

    @staticmethod
    @with_s3
    def get_metadata_file(s3, bucket, crawl_id, metadata):
        """Get a crawl metadata json file from the storage service"""
        try:
            file = s3.get_object(
                bucket, f"{crawl_id}/{METADATA_FOLDER_NAME}/{metadata}.json").read()
        except:
            return None
        return json.loads(file)


files = FileRepository()
