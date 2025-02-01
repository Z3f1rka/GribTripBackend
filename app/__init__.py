from fastapi import FastAPI

from app.api import user_router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(user_router)
    return app
