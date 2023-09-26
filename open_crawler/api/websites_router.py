from fastapi import APIRouter, HTTPException, status as statuscode
from pymongo.errors import DuplicateKeyError

import repositories
from api.utils import create_crawl, start_crawl
from models.request import UpdateWebsiteRequest, CreateWebsiteRequest
from models.website import WebsiteModel, ListWebsiteResponse

websites_router = APIRouter(
    prefix="/api/websites",
    tags=["websites"],
    responses={404: {"description": "Not found"}},
)


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
    try:
        repositories.websites.create(website)
    except DuplicateKeyError as e:
        raise HTTPException(
            status_code=statuscode.HTTP_409_CONFLICT,
            detail="Website already exists.",
        ) from e

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
