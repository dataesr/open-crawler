import io
import os
from zipfile import ZipFile, ZIP_DEFLATED

from fastapi import HTTPException, APIRouter, status as statuscode
from fastapi.responses import StreamingResponse
from minio import Minio

import app.repositories as repositories
from app.api.utils import create_crawl, start_crawl
from app.models.crawl import CrawlModel, ListCrawlResponse

crawls_router = APIRouter(
    prefix="/api/websites",
    tags=["crawls"],
    responses={404: {"description": "Not found"}},
)


@crawls_router.post(
    "/{website_id}/crawls",
    response_model=CrawlModel,
    status_code=statuscode.HTTP_202_ACCEPTED,
    summary="Start a new crawl for an existing website, using stored configuration.",
)
def crawl_website(website_id: str):
    if website := repositories.websites.get(website_id):
        crawl = create_crawl(website)
        start_crawl(crawl)
        repositories.websites.refresh_next_crawl(crawl.website_id)
        return crawl
    else:
        raise HTTPException(
            status_code=statuscode.HTTP_404_NOT_FOUND,
            detail="Website not found",
        )


@crawls_router.get(
    "/{website_id}/crawls",
    response_model=ListCrawlResponse,
    status_code=statuscode.HTTP_200_OK,
    summary="Get all crawls for a website",
)
def list_crawls(
    website_id: str,
    skip: int = 0,
    limit: int = 10,
):
    crawls = repositories.crawls.list(
        website_id=website_id, skip=skip, limit=limit
    )
    return crawls


@crawls_router.get(
    "/{website_id}/crawls/{crawl_id}/files",
    status_code=statuscode.HTTP_200_OK,
    summary="Get a zip of all files from a crawl",
)
def get_crawl_files(website_id: str, crawl_id: str) -> StreamingResponse:
    """Zip the files from the storage service"""
    client = Minio(
        endpoint=os.environ["STORAGE_SERVICE_URL"],
        access_key=os.environ["STORAGE_SERVICE_USERNAME"],
        secret_key=os.environ["STORAGE_SERVICE_PASSWORD"],
        secure=os.environ.get("STORAGE_SERVICE_SECURE", False),
        region=os.environ.get("STORAGE_SERVICE_REGION", None),
    )

    bucket = os.environ["STORAGE_SERVICE_BUCKET_NAME"]
    zip_io = io.BytesIO()
    if not (crawl := repositories.crawls.get(website_id, crawl_id)):
        raise HTTPException(
            status_code=statuscode.HTTP_404_NOT_FOUND,
            detail="Crawl not found",
        )
    url = crawl.config.url.replace("https://", "").replace("http://", "")
    prefix = f"{crawl_id}"
    objects = client.list_objects(bucket, prefix=prefix, recursive=True)
    with ZipFile(zip_io, "a", ZIP_DEFLATED, False) as zipper:
        for obj in objects:
            file = client.get_object(bucket, obj.object_name).read()
            zipper.writestr(obj.object_name.strip(crawl_id), file)
    return StreamingResponse(
        iter([zip_io.getvalue()]),
        media_type="application/x-zip-compressed",
        headers={
            "Content-Disposition": f"attachment; filename={url}-{crawl_id}.zip"
        },
    )
