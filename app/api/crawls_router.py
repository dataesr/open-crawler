from fastapi import HTTPException, APIRouter, status as statuscode
from fastapi.responses import StreamingResponse

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
def get_crawl_files(crawl_id: str) -> StreamingResponse:
    """Zip the files from the storage service"""
    zip_io = repositories.files.zip_all_crawl_files(crawl_id)
    return StreamingResponse(
        iter([zip_io.getvalue()]),
        media_type="application/x-zip-compressed",
        headers={
            "Content-Disposition": f"attachment; filename={crawl_id}.zip"
        },
    )


@crawls_router.delete(
    "/{website_id}/crawls/{crawl_id}",
    status_code=statuscode.HTTP_204_NO_CONTENT,
    summary="Delete a crawl",
)
def delete_crawl(crawl_id: str) -> None:
    """Zip the files from the storage service"""
    return repositories.files.delete_all_crawl_files(crawl_id)
