from typing import Annotated

from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from http import HTTPStatus
from os import getenv
from passlib.context import CryptContext
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timedelta

from src.api.v1.auth.entities.user import User
from src.config.database.setup import get_session

authenticate_router = APIRouter()

JWT_SECRET = getenv("JWT_SECRET")
JWT_EXPIRATION_DAYS = getenv("JWT_EXPIRATION_DAYS")
JWT_ALGORITHM = getenv("JWT_ALGORITHM")


@authenticate_router.post("/")
async def authenticate_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(User).where(User.username == form_data.username)
    )
    user = result.first()[0]

    context = CryptContext(
        schemes=["sha512_crypt"], deprecated="auto", default="sha512_crypt"
    )
    password_matches = context.verify(form_data.password, user.hashed_password)
    if user is None or not password_matches:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Incorrect username or password."
        )

    expire = datetime.utcnow() + timedelta(days=int(JWT_EXPIRATION_DAYS))
    access_token = jwt.encode(
        {
            "user_id": user.id,
            "user_name": user.username,
            "user_role": user.role,
            "exp": expire,
        },
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )

    return {"token": access_token, "token_type": "bearer"}
