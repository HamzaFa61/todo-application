"""
Utility functions
"""
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    paramaters:
        - plain_password: str
        - hashed_password: str

    return:
        - True if password is verified
        - False if password is not verified
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    parameters:
        - password: str

    return:
        - password_hash: str
    """
    return pwd_context.hash(password)
