from fastapi import APIRouter

from auth.v1.routes import auth_v1_router
from core.healthcheck import healthcheck_router
from users.v1.routes import users_v1_router

api_router = APIRouter(prefix="/api")

api_router.include_router(healthcheck_router)
api_router.include_router(auth_v1_router)
api_router.include_router(users_v1_router)
