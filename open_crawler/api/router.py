import io
import os
from zipfile import ZipFile, ZIP_DEFLATED

from celery import chain, group
from fastapi import APIRouter, HTTPException, status as statuscode
from fastapi.responses import StreamingResponse
from minio import Minio

import repositories
from celery_broker.tasks import (
    start_crawl_process,
    upload_html,
    METADATA_TASK_REGISTRY,
)
from models.crawl import CrawlModel, ListCrawlResponse
from models.request import UpdateWebsiteRequest, CreateWebsiteRequest
from models.website import WebsiteModel, ListWebsiteResponse
from services import crawler_logger
from services.crawler_logger import logger

websites_router = APIRouter(
    prefix="/api/websites",
    tags=["websites"],
    responses={404: {"description": "Not found"}},
)


def create_crawl(website: WebsiteModel) -> CrawlModel:
    crawl: CrawlModel = CrawlModel(
        website_id=website.id,
        config=website.to_config(),
    )
    crawl.init_tasks()
    repositories.crawls.create(crawl)
    return crawl


def start_crawl(crawl: CrawlModel) -> None:
    crawler_logger.set_file(crawl.id)
    logger.info(
        f"New crawl process ({crawl.id}) for website {crawl.config.url}"
    )
    metadata_tasks = group(
        METADATA_TASK_REGISTRY.get(metadata).s()
        for metadata in crawl.enabled_metadata
    )
    chain(
        start_crawl_process.s(crawl),
        metadata_tasks,
        upload_html.si(crawl),
    ).apply_async(task_id=crawl.id)


@websites_router.post(
    "",
    response_model=WebsiteModel,
    status_code=statuscode.HTTP_201_CREATED,
    summary="Add a new website",
    description="Create a website, start a crawl and return the website read object",
    tags=["websites"],
)
def create_website(data: CreateWebsiteRequest):
    website = data.to_website_model()
    repositories.websites.create(website)

    crawl = create_crawl(website)
    start_crawl(crawl)
    return website


@websites_router.get(
    "",
    response_model=ListWebsiteResponse,
    status_code=statuscode.HTTP_200_OK,
    summary="List all websites",
    tags=["websites"],
)
def list_websites(
    query: str | None = None,
    skip: int = 0,
    limit: int = 10,
    tags: str | None = None,
    status: str | None = None,
    sort: str = "created_at",
):
    return repositories.websites.list(
        query=query, tags=tags, status=status, skip=skip, limit=limit, sort=sort
    )


@websites_router.get(
    "/{website_id}",
    response_model=WebsiteModel,
    status_code=statuscode.HTTP_200_OK,
    summary="Get a single website by its unique ID",
    tags=["websites"],
)
def get_website(website_id: str):
    if data := repositories.websites.get(website_id):
        return data
    else:
        raise HTTPException(
            status_code=statuscode.HTTP_404_NOT_FOUND,
            detail="Website not found",
        )


@websites_router.patch(
    "/{website_id}",
    status_code=statuscode.HTTP_204_NO_CONTENT,
    summary="Update a website by its unique ID",
    tags=["websites"],
)
def patch_website(website_id: str, data: UpdateWebsiteRequest) -> None:
    try:
        repositories.websites.update(website_id, data)
    except AssertionError as e:
        raise HTTPException(
            status_code=statuscode.HTTP_404_NOT_FOUND,
            detail="Website not found",
        ) from e


@websites_router.delete(
    "/{website_id}",
    status_code=statuscode.HTTP_204_NO_CONTENT,
    summary="Delete a website by its unique ID",
    tags=["websites"],
)
def delete_website(website_id: str):
    repositories.websites.delete(website_id)


@websites_router.post(
    "/{website_id}/crawls",
    response_model=CrawlModel,
    status_code=statuscode.HTTP_202_ACCEPTED,
    summary="Start a new crawl for an existing website, using stored configuration.",
    tags=["websites"],
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


@websites_router.get(
    "/{website_id}/crawls",
    response_model=ListCrawlResponse,
    status_code=statuscode.HTTP_200_OK,
    summary="Get all crawls for a website",
    tags=["websites"],
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


@websites_router.get(
    "/{website_id}/crawls/{crawl_id}/files",
    status_code=statuscode.HTTP_200_OK,
    summary="Get a zip of all files from a crawl",
    tags=["websites"],
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
    crawl = repositories.crawls.get(website_id, crawl_id)
    url = crawl.config.url.replace("https://", "").replace("http://", "")
    prefix = f"{url}{crawl_id}"
    objects = client.list_objects(bucket, prefix=prefix, recursive=True)
    with ZipFile(zip_io, "a", ZIP_DEFLATED, False) as zipper:
        for obj in objects:
            file = client.get_object(bucket, obj.object_name).read()
            zipper.writestr(obj.object_name, file)
    return StreamingResponse(
        iter([zip_io.getvalue()]),
        media_type="application/x-zip-compressed",
        headers={
            "Content-Disposition": f"attachment; filename={url}-{crawl_id}.zip"
        },
    )
