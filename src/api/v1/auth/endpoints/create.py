from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from sqlmodel import select

from src.api.v1.auth.entities.user import User
from src.config.database.setup import get_session

create_router = APIRouter()
context = CryptContext(
    schemes=["sha512_crypt"], deprecated="auto", default="sha512_crypt"
)


@create_router.post(
    "/users/",
    response_model=User,
    response_model_exclude={"hashed_password"},
    status_code=201,
)
async def create_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(User).where(User.username == form_data.username)
    )
    if result.first() is not None:
        raise HTTPException(
            status_code=400, detail=f"username {form_data.username} already registered"
        )

    hashed_password = context.hash(form_data.password)
    user = User(username=form_data.username, hashed_password=hashed_password)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
