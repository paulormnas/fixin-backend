from enum import Enum

from sqlmodel import SQLModel, Field


class UserRoleEnum(Enum):
    Admin = 1
    Customer = 2
    Employee = 3


class UserRole(SQLModel, table=True):
    __tablename__ = "user_role"
    id: int = Field(default=None, primary_key=True)
    role: str = Field(unique=True)


class User(SQLModel, table=True):
    id: int | None = Field(nullable=False, default=None, primary_key=True, index=True)
    username: str = Field(unique=True)
    hashed_password: str | None = Field(nullable=False)
    first_name: str = Field(default=None)
    last_name: str = Field(default=None)
    is_active: bool = Field(nullable=False, default=True)
    role: int = Field(
        nullable=False, default=UserRoleEnum.Customer.value, foreign_key="user_role.id"
    )


class Address(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    street: str = Field(default=None)
    city: str = Field(default=None)
    state: str = Field(default=None)
    complement: str = Field(default=None)
    zipcode: str = Field(default=None)


class Customer(SQLModel, table=True):
    user_id: int = Field(nullable=False, foreign_key="user.id", primary_key=True)
    address_id: int | None = Field(nullable=True, foreign_key="address.id")


class Employee(SQLModel, table=True):
    user_id: int = Field(nullable=False, foreign_key="user.id", primary_key=True)
    job_title: str | None = Field(nullable=True)
