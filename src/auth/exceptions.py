from fastapi import HTTPException
from http import HTTPStatus


class IncorrectUsernameOrPassword(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTPStatus.BAD_REQUEST, detail="Incorrect username or password."
        )
