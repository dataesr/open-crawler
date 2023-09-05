import logging
from celery import chain, group
from fastapi import APIRouter,  HTTPException, status as statuscode

import repositories
from celery_broker.tasks import start_crawl_process, upload_html, METADATA_TASK_REGISTRY
from models.crawl import CrawlProcess
from models.website import CreateWebsiteRequest, WebsiteModel, UpdateWebsiteRequest

websites_router = APIRouter(
    prefix="/api/websites", tags=["websites"], responses={404: {"description": "Not found"}})

logger = logging.getLogger(__name__)


@websites_router.post(
    "",
    response_model=WebsiteModel,
    status_code=statuscode.HTTP_201_CREATED,
    summary="Add a new website",
    description="Create a website, start a crawl and return the website read object",
    tags=["websites"]
)
def create(data: CreateWebsiteRequest):
    website = data.to_website_model()
    repositories.websites.create(website)
    crawl: CrawlProcess = CrawlProcess(
        website_id=website.id, config=website.to_config())
    repositories.crawls.create(crawl)
    metadata_tasks = group(METADATA_TASK_REGISTRY.get(metadata).s()
                           for metadata in crawl.enabled_metadata)
    chain(
        start_crawl_process.s(crawl),
        metadata_tasks,
        upload_html.si(crawl),
    ).apply_async(task_id=crawl.id)

    return website


@websites_router.get(
    "",
    response_model=list[WebsiteModel],
    summary="List all websites",
    tags=["websites"]
)
def list_websites(query: str = None, skip: int = 0, limit: int = 10, tags: list[str] = None, status: list[str] = None):
    return repositories.websites.list(query=query, tags=tags, status=status, skip=skip, limit=limit)


@websites_router.get(
    "/{id}",
    response_model=WebsiteModel,
    summary="Get a single website by its unique ID",
    tags=["websites"]
)
def get_website(id: str):
    data = repositories.websites.get(id)
    if not data:
        raise HTTPException(
            status_code=statuscode.HTTP_404_NOT_FOUND, detail="Website not found")
    return data


@websites_router.patch(
    "/{id}",
    status_code=statuscode.HTTP_204_NO_CONTENT,
    summary="Update a website by its unique ID",
    tags=["websites"]
)
def patch_website(id: str, data: UpdateWebsiteRequest) -> None:
    repositories.websites.update(id, data)
    return {}


@websites_router.delete(
    "/{id}",
    status_code=statuscode.HTTP_204_NO_CONTENT,
    summary="Delete a website by its unique ID",
    tags=["websites"]
)
def delete_website(id: str):
    repositories.websites.delete(id)
    return {}


@websites_router.post(
    "/{id}/crawls",
    response_model=CrawlProcess,
    status_code=statuscode.HTTP_202_ACCEPTED,
    summary="Start a new crawl for a website",
    tags=["websites"]
)
def crawl_website(id: str):
    website = repositories.websites.get(id)
    crawl: CrawlProcess = CrawlProcess(
        website_id=website.id, config=website.to_config())
    repositories.crawls.create(crawl)
    metadata_tasks = group(METADATA_TASK_REGISTRY.get(metadata).s()
                           for metadata in crawl.enabled_metadata)
    chain(
        start_crawl_process.s(crawl),
        metadata_tasks,
        upload_html.si(crawl),
    ).apply_async(task_id=crawl.id)
    return crawl


@websites_router.get(
    "/{id}/crawls",
    response_model=list[CrawlProcess],
    status_code=statuscode.HTTP_200_OK,
    summary="Get all crawls for a website",
    tags=["websites"]
)
def list_crawls(id: str):
    crawls = repositories.crawls.list(website_id=id)
    return crawls
