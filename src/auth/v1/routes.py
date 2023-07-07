from typing import Annotated

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, APIRouter
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.services import signin_user, signup_user
from src.config.database.setup import get_db_session

auth_v1_router = APIRouter(prefix="/v1/auth")


@auth_v1_router.post("/signin/")
async def signin(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db_session: AsyncSession = Depends(get_db_session),
):
    return await signin_user(form_data.username, form_data.password, db_session)


@auth_v1_router.post("/signup/", status_code=201)
async def signup(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db_session: AsyncSession = Depends(get_db_session),
):
    return await signup_user(form_data.username, form_data.password, db_session)
