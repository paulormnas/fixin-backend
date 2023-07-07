from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, APIRouter, Header
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config.database.setup import get_db_session
from src.users.schemas import NewCustomer, NewEmployee, ResponseUser
from src.users.service import (
    get_users,
    check_authorization,
    create_customer,
    create_employee,
)

users_v1_router = APIRouter(prefix="/v1/users")
context = CryptContext(
    schemes=["sha512_crypt"], deprecated="auto", default="sha512_crypt"
)


@users_v1_router.get("/", response_model=list[ResponseUser])
async def list_users(
    authorization: Annotated[str | None, Header()] = None,
    db_session: AsyncSession = Depends(get_db_session),
):
    is_authorized = await check_authorization(authorization)
    if is_authorized:
        return await get_users(db_session)


@users_v1_router.post(
    "/customer/",
    response_model=NewCustomer,
    response_model_exclude={"address_id"},
    status_code=HTTPStatus.CREATED,
)
async def post_customer(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    authorization: Annotated[str | None, Header()] = None,
    db_session: AsyncSession = Depends(get_db_session),
):
    is_authorized = await check_authorization(authorization)
    if is_authorized:
        customer = await create_customer(
            username=form_data.username,
            password=form_data.password,
            db_session=db_session,
        )
        return customer


@users_v1_router.post(
    "/employee/",
    response_model=NewEmployee,
    response_model_exclude={"hashed_password"},
    status_code=HTTPStatus.CREATED,
)
async def post_employee(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    authorization: Annotated[str | None, Header()] = None,
    db_session: AsyncSession = Depends(get_db_session),
):
    is_authorized = await check_authorization(authorization)
    if is_authorized:
        employee = await create_employee(
            username=form_data.username,
            password=form_data.password,
            db_session=db_session,
        )
        return employee
