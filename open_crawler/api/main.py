from api.utils import create_api_app

api_app = create_api_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:api_app", port=9000, reload=True)
