from http import HTTPStatus

from fastapi import HTTPException


class InvalidUsername(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Username is invalid or already registered",
        )


class Unauthorized(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Invalid token",
        )


class Forbidden(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Token bearer cannot execute the required operation",
        )
