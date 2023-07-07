from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.exceptions import IncorrectUsernameOrPassword
from src.auth.schemas import AuthenticatedUser
from src.core.exceptions import InvalidUsername
from src.core.middlewares.AuthenticationMiddleware import create_token
from src.core.models import User
from src.users.service import create_customer, get_user_by_username
from passlib.hash import pbkdf2_sha512


async def signin_user(
    username: str, password: str, db_session: AsyncSession
) -> AuthenticatedUser:
    user: User = await get_user_by_username(username, db_session)

    if user is None:
        raise IncorrectUsernameOrPassword()

    password_matches = pbkdf2_sha512.verify(password, user.hashed_password)
    if not password_matches:
        raise IncorrectUsernameOrPassword()

    access_token = await create_token(user.id, user.username, user.role)

    auth_user = AuthenticatedUser(
        id=user.id,
        token=access_token,
    )
    return auth_user


async def signup_user(
    username: str, password: str, db_session: AsyncSession
) -> AuthenticatedUser:
    user: User = await get_user_by_username(username, db_session)

    if user is not None:
        raise InvalidUsername()

    customer = await create_customer(username, password, db_session)

    access_token = await create_token(customer.id, customer.username, customer.role)
    auth_user = AuthenticatedUser(
        id=customer.id,
        token=access_token,
    )
    return auth_user
