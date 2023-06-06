from fastapi import APIRouter

from src.api.v1.auth.endpoints.authentication_user import authenticate_router
from src.api.v1.auth.endpoints.list import list_router
from src.api.v1.auth.endpoints.create import create_router

auth_router = APIRouter(prefix="/auth")

auth_router.include_router(authenticate_router)
auth_router.include_router(list_router)
auth_router.include_router(create_router)
