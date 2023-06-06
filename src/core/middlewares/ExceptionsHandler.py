import sentry_sdk
from os import getenv
from http.client import INTERNAL_SERVER_ERROR

from fastapi.responses import JSONResponse

from dotenv import load_dotenv

from src.core.exceptions import AppException

load_dotenv()


async def error_handler_middleware(request, e):
    sentry_sdk.capture_exception(e)

    ENVIRONMENT = getenv("ENV", None)
    if ENVIRONMENT == "development":
        print(e)

    if isinstance(e, AppException):
        return JSONResponse(
            status_code=e.status, content={"detail": e.slug, "message": e.message}
        )
    return JSONResponse(
        status_code=INTERNAL_SERVER_ERROR,
        media_type="application/json",
        content={
            "message": "An unidentified error has ocurred.",
        },
    )
