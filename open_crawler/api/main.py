import uvicorn as uvicorn

from open_crawler.api.utils import create_api_app

api_app = create_api_app()


if __name__ == "__main__":
    uvicorn.run("main:api_app", port=9000, reload=True)
