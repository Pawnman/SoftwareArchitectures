import json
from typing import Annotated

from aiocircuitbreaker import circuit
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi_cache.decorator import cache
from redis.asyncio.client import Redis
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from database.postgres_db import get_async_session
from crud import update_user, get_user, delete_user, init_redis_pool, obj_to_dict, get_user_by_id
from utils.helpers import get_current_active_user
from models import User
from schemas.user_schemas import UserReadSchema, UserUpdateSchema

router = APIRouter(
    tags=['user'],
    prefix='/user',

)


@router.get('/me', status_code=status.HTTP_200_OK, response_model=UserReadSchema)
@cache(expire=300)
@circuit(failure_threshold=5, recovery_timeout=30)
async def get_me(current_user: Annotated[User, Depends(get_current_active_user)]):

    return current_user


@router.patch('/me', response_model=UserReadSchema, status_code=status.HTTP_202_ACCEPTED)
@circuit(failure_threshold=5, recovery_timeout=30)
async def update_me(new_data: UserUpdateSchema, current_user: Annotated[User, Depends(get_current_active_user)],
                    session: AsyncSession = Depends(get_async_session), redis: Redis = Depends(init_redis_pool)):
    new_data = new_data.model_dump(exclude_none=True)

    await update_user(user=current_user, data=new_data, session=session)

    user = await get_user(current_user.username)

    key = user.id
    value = UserReadSchema.model_validate(obj_to_dict(user))
    await redis.set(key, json.dumps(value.model_dump()), 5 * 60)

    return user


@router.delete('/me', status_code=status.HTTP_204_NO_CONTENT)
@circuit(failure_threshold=5, recovery_timeout=30)
async def delete_me(current_user: Annotated[User, Depends(get_current_active_user)],
                    session: AsyncSession = Depends(get_async_session), redis: Redis = Depends(init_redis_pool)):

    await delete_user(user=current_user, session=session)

    await redis.delete(current_user.id)

    return {'message': 'User deleted'}


@router.get('/search/{mask}', response_model=UserReadSchema, dependencies=[Depends(get_current_active_user)])
@cache(expire=300)
@circuit(failure_threshold=5, recovery_timeout=30)
async def get_user_by_mask(mask: str, session: AsyncSession = Depends(get_async_session)):

    try:
        stmt = select(User).filter(or_(User.name.contains('%' + mask + '%'),
                                   User.last_name.contains('%' + mask + '%')))

        user = await session.execute(stmt)
        user = user.scalar()

        if user:
            return user
        else:
            raise HTTPException(status_code=404, detail='User not found')

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/', response_model=UserReadSchema, dependencies=[Depends(get_current_active_user)])
@cache(expire=300)
@circuit(failure_threshold=5, recovery_timeout=30)
async def get_user_by_username(username: str):

    try:

        if user := await get_user(username):
            return user
        else:
            raise HTTPException(status_code=404, detail='User not found')

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/get/{user_id}', response_model=UserReadSchema, dependencies=[Depends(get_current_active_user)])
@cache(expire=300)
@circuit(failure_threshold=5, recovery_timeout=30)
async def search_user(user_id: int, session: AsyncSession = Depends(get_async_session)):

    user = await get_user_by_id(user_id=user_id, session=session)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")

    return user