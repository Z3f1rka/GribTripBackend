from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import admin_router
from app.api import comment_router
from app.api import history_router
from app.api import route_router
from app.api import user_router


# TODO: настроить нормально CORS
def create_app() -> FastAPI:
    app = FastAPI()
    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(user_router)
    app.include_router(route_router)
    app.include_router(admin_router)
    app.include_router(comment_router)
    app.include_router(history_router)
    return app
