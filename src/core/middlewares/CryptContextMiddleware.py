from passlib.context import CryptContext


def get_crypt_context() -> CryptContext:
    return CryptContext(
        schemes=["sha512_crypt"], deprecated="auto", default="sha512_crypt"
    )
