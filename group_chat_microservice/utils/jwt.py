from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from settings import settings

SECRET_KEY = settings.SECRET_KEY_AUTH
ALGORITHM = "HS256"
ACCESS_TOKEN_TYPE = 'access'

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

TOKEN_EXCEPTION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Invalid token",
)


def get_current_token_payload(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        return jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )

    except JWTError:
        raise TOKEN_EXCEPTION


async def get_username_by_token_sub(payload: dict):
    username: str = payload.get("sub")

    if username is None:
        raise CREDENTIALS_EXCEPTION

    return username


class UserGetterFromToken:
    def __init__(self, token_type: str):
        self.token_type = token_type

    async def __call__(self, payload: dict = Depends(get_current_token_payload)):
        await validate_token_type(payload, self.token_type)
        return await get_username_by_token_sub(payload)


async def validate_token_type(payload: dict, token_type: str) -> bool:
    current_token_type = payload.get("type")

    if current_token_type == token_type:
        return True

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Invalid token type {current_token_type!r} expected {token_type!r}",
    )


get_current_auth_user = UserGetterFromToken(ACCESS_TOKEN_TYPE)
