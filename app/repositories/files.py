import io
import json
from zipfile import ZipFile, ZIP_DEFLATED
from app.s3 import with_s3


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
    def store_html_file(s3, bucket, object_name, file_path, content_type):
        """Store a crawl file in the storage service"""
        return s3.fput_object(bucket, object_name=object_name, file_path=file_path, content_type=content_type)

    @staticmethod
    @with_s3
    def store_metadata_file(s3, bucket, crawl_id, object_name, content_type, data):
        """Store a crawl file in the storage service"""
        object_path = f"{crawl_id}/metadata/{object_name}"
        # Convert the string to bytes
        data_bytes = data.encode('utf-8')
        # Create a BytesIO object to make the bytes readable
        data_stream = io.BytesIO(data_bytes)
        return s3.put_object(bucket, object_name=object_path, length=len(data_bytes), content_type=content_type, data=data_stream)

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
                bucket, f"{crawl_id}/metadata/{metadata}.json").read()
        except:
            return None
        return json.loads(file)


files = FileRepository()
