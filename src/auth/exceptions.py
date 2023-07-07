from http import HTTPStatus
from fastapi import HTTPException


class IncorrectUsernameOrPassword(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTPStatus.BAD_REQUEST, detail="Incorrect username or password."
        )
