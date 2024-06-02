from fastapi import HTTPException, status
from crud import get_user
from utils.jwt import pwd_context
from schemas.user_schemas import UserInDBSchema


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(username: str, password: str):
    user = await get_user(username=username)

    if not user:
        return False
    if not verify_password(password, UserInDBSchema.model_validate(user).hashed_password):
        return False
    return user


async def validate_token_type(payload: dict, token_type: str) -> bool:
    current_token_type = payload.get("type")

    if current_token_type == token_type:
        return True

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Invalid token type {current_token_type!r} expected {token_type!r}",
    )
