from fastapi.params import Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config.database.setup import get_db_session
from src.core.exceptions import InvalidUsername, Unauthorized
from src.core.middlewares.AuthenticationMiddleware import validate_token
from src.core.middlewares.CryptContextMiddleware import get_crypt_context
from src.core.models import User, Customer, UserRoleEnum, Employee
from src.users.schemas import NewCustomer, NewEmployee

context = get_crypt_context()


def check_authorization(authorization: str) -> bool:
    if authorization is None:
        raise Unauthorized()

    token = authorization.split()[1]
    token_user = await validate_token(token)
    if token_user.role is not UserRoleEnum.Admin.value:
        raise Unauthorized()

    return True


def get_users(db_session: AsyncSession = Depends(get_db_session)) -> list[User]:
    result = await db_session.execute(select(User))
    user: list[User] = result.scalar()
    return user


def get_user_by_username(
    username: str, db_session: AsyncSession = Depends(get_db_session)
) -> User | None:
    result = await db_session.execute(select(User).where(User.username == username))
    user: User = result.scalar_one_or_none()
    return user


def create_user(
    username: str,
    password: str,
    role: int = UserRoleEnum.Customer.value,
    db_session: AsyncSession = Depends(get_db_session),
) -> User:
    user = get_user_by_username(username)
    if user is not None:
        raise InvalidUsername()

    hashed_password = context.hash(password)
    user = User(username=username, hashed_password=hashed_password, role=role)
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


def create_customer(
    username: str, password: str, db_session: AsyncSession = Depends(get_db_session)
) -> NewCustomer:
    user = create_user(
        username=username, password=password, role=UserRoleEnum.Customer.value
    )

    customer = Customer(user_id=user.id)
    db_session.add(customer)
    await db_session.commit()
    await db_session.refresh(customer)
    return NewCustomer(id=user.id, role=user.role, username=user.username)


def create_employee(
    username: str, password: str, db_session: AsyncSession = Depends(get_db_session)
) -> NewEmployee:
    user = create_user(
        username=username, password=password, role=UserRoleEnum.Employee.value
    )

    employee = Employee(user_id=user.id)
    db_session.add(employee)
    await db_session.commit()
    await db_session.refresh(employee)
    return NewEmployee(id=user.id, username=user.username)
