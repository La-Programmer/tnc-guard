from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from database import connect_to_mongo
from core.handlers.exception_handler import global_exception_handler
from core.config import settings


class APIInfo(BaseModel):
    title: str = "T&C Guard API"
    swagger: str = "v1"
    description: str = "API documentation for T&C Guard"
    version: str = "v1"
    contact: dict = {"name": "Justin Ebedi", "email": "justinoghenekomeebedi@gmail.com"}
    license_info: dict = {"name": "MIT License"}


def create_app():
    api_info = APIInfo()

    docs_url = "/docs" if settings.ENV.lower() != "prod" else None
    redoc_url = "/redoc" if settings.ENV.lower() != "prod" else None
    openapi_url = "/openapi.json" if settings.ENV.lower() != "prod" else None

    app = FastAPI(
        title=api_info.title,
        description=api_info.description,
        version=api_info.version,
        contact=api_info.contact,
        license_info=api_info.license_info,
        docs_url=docs_url,
        redoc_url=redoc_url,
        openapi_url=openapi_url,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )

    @app.exception_handler(HTTPException)
    def http_exception_handler(request, exc: HTTPException):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    connect_to_mongo(settings.MONGODB_NAME)

    app.add_exception_handler(Exception, global_exception_handler)

    return app
