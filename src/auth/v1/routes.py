from typing import Annotated

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, APIRouter
from src.auth.services import signin, signup

auth_v1_router = APIRouter(prefix="/auth")


@auth_v1_router.post("/signin/")
async def signin(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    return signin(form_data)


@auth_v1_router.post("/signup/", status_code=201)
async def signup(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    return signup(form_data)
