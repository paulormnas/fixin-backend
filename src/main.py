import json
from os import getenv

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api import api_router
from core.middlewares.ExceptionsHandler import error_handler_middleware
from config.database.setup import get_db_session

app = FastAPI()


@app.exception_handler(HTTPException)
async def validation_exception_handler(request, e):
    return await error_handler_middleware(request, e)


ENVIRONMENT = getenv("ENV", None)

if ENVIRONMENT in ["production", "staging"]:
    import sentry_sdk

    sentry_dsn = getenv("SENTRY_DSN", None)

    if sentry_dsn:
        SAMPLE_RATE = getenv("SENTRY_SAMPLE_RATE", 0)

        sentry_sdk.init(
            dsn=sentry_dsn,
            traces_sample_rate=float(SAMPLE_RATE),
        )


origins = json.loads(getenv("CORS_ORIGINS"))
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router, dependencies=[Depends(get_db_session)])
