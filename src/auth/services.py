from typing import Annotated

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends

from src.auth.exceptions import IncorrectUsernameOrPassword
from src.auth.schemas import AuthenticatedUser
from src.core.exceptions import InvalidUsername
from src.core.middlewares.AuthenticationMiddleware import create_token
from src.core.middlewares.CryptContextMiddleware import get_crypt_context
from src.core.models import User
from src.users.service import create_customer, get_user_by_username

context = get_crypt_context()


async def signin(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user: User = get_user_by_username(form_data.username)

    if user is None:
        raise IncorrectUsernameOrPassword()

    password_matches = context.verify(form_data.password, user.hashed_password)
    if not password_matches:
        raise IncorrectUsernameOrPassword()

    access_token = await create_token(user.id, user.username, user.role)

    auth_user = AuthenticatedUser(
        id=user.id,
        token=access_token,
    )
    return auth_user


async def signup(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> AuthenticatedUser:
    user: User = get_user_by_username(form_data.username)

    if user is not None:
        raise InvalidUsername()

    customer = create_customer(form_data.username, form_data.password)

    access_token = await create_token(customer.id, customer.username, customer.role)
    auth_user = AuthenticatedUser(
        id=customer.id,
        token=access_token,
    )
    return auth_user
