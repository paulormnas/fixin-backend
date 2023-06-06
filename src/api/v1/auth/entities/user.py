from enum import Enum

from sqlmodel import SQLModel, Field


class UserRole(Enum):
    Admin = "admin"
    Employee = "employee"
    Customer = "customer"


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    hashed_password: str = Field(nullable=False)
    name: str = Field(default=None)
    is_active: bool = Field(nullable=False, default=True)
    role: str = Field(nullable=False, default=UserRole.Customer.value)


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: str | None = None
