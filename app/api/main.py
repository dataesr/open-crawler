from app.api.factory import create_api_app

api_app = create_api_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api.main:api_app", port=9000, reload=True)
