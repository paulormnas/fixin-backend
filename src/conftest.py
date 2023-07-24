import os
from datetime import datetime, timedelta

import pytest
import pytest_asyncio
from httpx import AsyncClient
from dotenv import load_dotenv
from jose import jwt
from passlib.handlers.pbkdf2 import pbkdf2_sha512
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel

from src.auth.services import signin_user
from src.config.database.setup import get_db_session
from src.core.models import User, UserRoleEnum, Customer, UserRole
from src.main import app
from src.users.service import create_customer
from src.vehicles.models import Vehicle

load_dotenv("src/config/.env")

JWT_EXPIRATION_DAYS = os.getenv("JWT_EXPIRATION_DAYS")
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

TEST_SQLALCHEMY_DATABASE_URL = os.environ.get("TEST_DATABASE_URL", None)
ENVIRONMENT = os.environ.get("ENV", None)

db_logs = "debug" if ENVIRONMENT == "development" else True


@pytest_asyncio.fixture
async def db_engine():
    engine = create_async_engine(TEST_SQLALCHEMY_DATABASE_URL, echo=db_logs)
    yield engine


@pytest_asyncio.fixture
async def db_connection(db_engine):
    async with db_engine.connect() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
        yield conn
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session(db_connection) -> AsyncSession:
    async_session = sessionmaker(
        bind=db_connection, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture
async def setup_db(db_session):
    user_role_admin = UserRole(id=UserRoleEnum.Admin.value, role="admin")
    user_role_customer = UserRole(id=UserRoleEnum.Customer.value, role="customer")
    user_role_employee = UserRole(id=UserRoleEnum.Employee.value, role="employee")
    db_session.add(user_role_admin)
    db_session.add(user_role_customer)
    db_session.add(user_role_employee)
    await db_session.commit()


@pytest_asyncio.fixture
async def client(db_session, setup_db) -> AsyncClient:
    app.dependency_overrides[get_db_session] = lambda: db_session
    async with AsyncClient(
        app=app, base_url="http://test", headers={"X-User-Fingerprint": "Test"}
    ) as client:
        yield client


@pytest.fixture
def user_payload():
    return {"username": "john.doe@email.com", "password": "test123"}


@pytest.fixture
def user2_payload():
    return {"username": "alicia.doe@email.com", "password": "test456"}


@pytest.fixture
def admin_payload():
    return {"username": "alex.doe@email.com", "password": "test789"}


@pytest.fixture
def customer(db_session, user_payload):
    async def _customer():
        customer = await create_customer(
            user_payload.get("username"), user_payload.get("password"), db_session
        )
        return customer

    return _customer


@pytest_asyncio.fixture
async def admin(db_session, admin_payload):
    password = admin_payload["password"]
    hashed_password = pbkdf2_sha512.hash(password)
    admin = User(
        username=admin_payload["username"],
        hashed_password=hashed_password,
        role=UserRoleEnum.Admin.value,
    )
    db_session.add(admin)
    await db_session.commit()
    await db_session.refresh(admin)
    return admin


@pytest.fixture
def admin_token(db_session, admin, admin_payload):
    async def _token():
        auth_admin = await signin_user(
            username=admin_payload["username"],
            password=admin_payload["password"],
            db_session=db_session,
        )
        return auth_admin.token

    return _token


@pytest.fixture
def user_token(db_session, customer, user_payload):
    async def _token():
        await customer()
        auth_user = await signin_user(
            username=user_payload["username"],
            password=user_payload["password"],
            db_session=db_session,
        )
        return auth_user.token

    return _token


@pytest.fixture
def expired_token(admin):
    async def _expired_token():
        expire = datetime.utcnow() - timedelta(days=int(JWT_EXPIRATION_DAYS))
        expired_token = jwt.encode(
            {
                "user_id": admin.id,
                "username": admin.username,
                "user_role": admin.role,
                "exp": expire,
            },
            JWT_SECRET,
            algorithm=JWT_ALGORITHM,
        )
        return expired_token

    return _expired_token


@pytest.fixture
def vehicle_payload():
    return {
        "id": 1,
        "brand": "chevrolet",
        "model": "corsa",
        "color": "black",
        "year": "2007",
    }


@pytest_asyncio.fixture
async def vehicle(db_session, vehicle_payload):
    test_vehicle = Vehicle(
        brand=vehicle_payload["brand"],
        model=vehicle_payload["model"],
        color=vehicle_payload["color"],
        year=vehicle_payload["year"],
    )
    db_session.add(test_vehicle)
    await db_session.commit()
    await db_session.refresh(test_vehicle)
    return test_vehicle
