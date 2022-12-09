from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_string(str_to_hash: str) -> str:
    hashed_string = pwd_context.hash(str_to_hash)

    return hashed_string
