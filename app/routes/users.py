# routes/users.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from uuid import UUID
from typing import List

from ..database import get_session
from ..models import User
from ..schemas import UserOut, UserCreate, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])

# Create user
@router.post("/users", response_model=UserOut)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    new_user = User(**user.dict())
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user

# Get all users
@router.get("/users", response_model=List[UserOut])
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users


# Get user by id
@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: UUID, session: AsyncSession = Depends(get_session)):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Update user
@router.put("/{user_id}", response_model=UserOut)
async def update_user(user_id: UUID, updates: UserUpdate, session: AsyncSession = Depends(get_session)):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in updates.dict(exclude_unset=True).items():
        setattr(user, key, value)

    await session.commit()
    await session.refresh(user)
    return user


# Delete user
@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: UUID, session: AsyncSession = Depends(get_session)):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await session.delete(user)
    await session.commit()
    return
