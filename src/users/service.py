from fastapi.params import Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config.database.setup import get_db_session
from src.core.exceptions import InvalidUsername, Unauthorized
from src.core.middlewares.AuthenticationMiddleware import validate_token
from src.core.models import User, Customer, UserRoleEnum, Employee
from src.users.schemas import NewCustomer, NewEmployee
from passlib.hash import pbkdf2_sha512


async def check_authorization(authorization: str) -> bool:
    if authorization is None:
        raise Unauthorized()

    token = authorization.split()[1]
    token_user = await validate_token(token)
    if token_user.role is not UserRoleEnum.Admin.value:
        raise Unauthorized()

    return True


async def get_users(db_session: AsyncSession) -> list[User]:
    result = await db_session.execute(select(User))
    user: list[User] = result.scalar()
    return user


async def get_user_by_username(username: str, db_session: AsyncSession) -> User | None:
    result = await db_session.execute(select(User).where(User.username == username))
    user: User = result.scalar_one_or_none()
    return user


async def create_user(
    username: str,
    password: str,
    db_session: AsyncSession,
    role: int = UserRoleEnum.Customer.value,
) -> User:
    user = await get_user_by_username(username, db_session)
    if user is not None:
        raise InvalidUsername()

    hashed_password = pbkdf2_sha512.hash(password)
    user = User(username=username, hashed_password=hashed_password, role=role)
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


async def create_customer(
    username: str, password: str, db_session: AsyncSession
) -> NewCustomer:
    user = await create_user(
        username=username,
        password=password,
        role=UserRoleEnum.Customer.value,
        db_session=db_session,
    )

    customer = Customer(user_id=user.id)
    db_session.add(customer)
    await db_session.commit()
    await db_session.refresh(customer)
    return NewCustomer(id=user.id, role=user.role, username=user.username)


async def create_employee(
    username: str, password: str, db_session: AsyncSession = Depends(get_db_session)
) -> NewEmployee:
    user = await create_user(
        username=username,
        password=password,
        role=UserRoleEnum.Employee.value,
        db_session=db_session,
    )

    employee = Employee(user_id=user.id)
    db_session.add(employee)
    await db_session.commit()
    await db_session.refresh(employee)
    return NewEmployee(id=user.id, username=user.username)
