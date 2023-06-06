from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, APIRouter, Header
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from src.users.schemas import NewCustomer, NewEmployee, ResponseUser
from src.users.service import get_users, check_authorization

users_v1_router = APIRouter(prefix="/v1/users")
context = CryptContext(
    schemes=["sha512_crypt"], deprecated="auto", default="sha512_crypt"
)


@users_v1_router.get("/", response_model=list[ResponseUser])
async def read_users(
    authorization: Annotated[str | None, Header()] = None,
):
    is_authorized = check_authorization(authorization)
    if is_authorized:
        return get_users()


@users_v1_router.post(
    "/customer/",
    response_model=NewCustomer,
    response_model_exclude={"address_id"},
    status_code=HTTPStatus.CREATED,
)
async def create_customer(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    authorization: Annotated[str | None, Header()] = None,
):
    is_authorized = check_authorization(authorization)
    if is_authorized:
        customer = create_customer(
            username=form_data.username, password=form_data.password
        )
        return customer


@users_v1_router.post(
    "/employee/",
    response_model=NewEmployee,
    response_model_exclude={"hashed_password"},
    status_code=HTTPStatus.CREATED,
)
async def create_employee(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    authorization: Annotated[str | None, Header()] = None,
):
    is_authorized = check_authorization(authorization)
    if is_authorized:
        employee = create_employee(
            username=form_data.username, password=form_data.password
        )
        return employee
