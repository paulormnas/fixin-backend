from fastapi import Depends, APIRouter
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.auth.entities.user import User
from src.config.database.setup import get_session

list_router = APIRouter()


@list_router.get("/users/", response_model=list[User])
async def read_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return [
        User(email=user.email, password=user.password, id=user.id) for user in users
    ]
