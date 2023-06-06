from pydantic import BaseModel


class NewCustomer(BaseModel):
    id: int
    role: int
    username: str


class NewEmployee(BaseModel):
    id: int
    username: str


class ResponseUser(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    is_active: bool
    role: int
