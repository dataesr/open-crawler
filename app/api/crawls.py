from fastapi import HTTPException, APIRouter, status as statuscode
from fastapi.responses import StreamingResponse

from app.repositories.crawls import crawls
from app.repositories.files import files
from app.repositories.websites import websites
from app.api.utils import start_crawl
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
    if website := websites.get(website_id):
        crawl = website.to_crawl()
        crawls.create(crawl)
        start_crawl(crawl)
        websites.refresh_next_crawl(crawl.website_id)
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
    crawls_list = crawls.list(
        website_id=website_id, skip=skip, limit=limit
    )
    return crawls_list


@crawls_router.get(
    "/{website_id}/crawls/{crawl_id}/files",
    status_code=statuscode.HTTP_200_OK,
    summary="Get a zip of all files from a crawl",
)
def get_crawl_files(crawl_id: str) -> StreamingResponse:
    """Zip the files from the storage service"""
    zip_io = files.zip_all_crawl_files(crawl_id)
    return StreamingResponse(
        iter([zip_io.getvalue()]),
        media_type="application/x-zip-compressed",
        headers={
            "Content-Disposition": f"attachment; filename={crawl_id}.zip"
        },
    )


@crawls_router.get(
    "/{website_id}/crawls/{crawl_id}/metadata/{metadata}",
    status_code=statuscode.HTTP_200_OK,
    summary="Get a crawl metadata result",
)
def get_metadata_file(crawl_id: str, metadata):
    """Get a crawl metadata json file from the storage service and return it as a JSON response"""
    if result := files.get_metadata_file(crawl_id, metadata):
        return result
    else:
        raise HTTPException(
            status_code=statuscode.HTTP_404_NOT_FOUND,
            detail="Metadata file not found",
        )


@crawls_router.delete(
    "/{website_id}/crawls/{crawl_id}",
    status_code=statuscode.HTTP_204_NO_CONTENT,
    summary="Delete a crawl",
)
def delete_crawl(crawl_id: str) -> None:
    """Zip the files from the storage service"""
    files.delete_all_crawl_files(crawl_id)
    crawls.delete(crawl_id)
