# routes/users.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from ..database import get_session
from ..models import User
from ..schemas import UserOut

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/users")
async def create_user(name: str, email: str, role: str, 
    unit_number:str, session: AsyncSession = Depends(get_session)):
    user = User(name=name, email=email, role=role, unit_number=unit_number)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

@router.get("/users", response_model=List[UserOut])
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users
