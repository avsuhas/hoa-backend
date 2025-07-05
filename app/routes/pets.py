# routes/pet_info.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from ..database import get_session
from ..models import PetInfo
from ..schemas import PetInfoCreate, PetInfoUpdate, PetInfoOut

router = APIRouter(prefix="/pets", tags=["Pet Info"])

@router.post("/", response_model=PetInfoOut)
async def create_pet(pet: PetInfoCreate, session: AsyncSession = Depends(get_session)):
    new_pet = PetInfo(**pet.dict())
    session.add(new_pet)
    await session.commit()
    await session.refresh(new_pet)
    return new_pet

@router.get("/", response_model=List[PetInfoOut])
async def list_pets(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(PetInfo))
    return result.scalars().all()

@router.get("/{pet_id}", response_model=PetInfoOut)
async def get_pet(pet_id: int, session: AsyncSession = Depends(get_session)):
    pet = await session.get(PetInfo, pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet

@router.put("/{pet_id}", response_model=PetInfoOut)
async def update_pet(pet_id: int, updates: PetInfoUpdate, session: AsyncSession = Depends(get_session)):
    pet = await session.get(PetInfo, pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(pet, key, value)

    await session.commit()
    await session.refresh(pet)
    return pet

@router.delete("/{pet_id}", status_code=204)
async def delete_pet(pet_id: int, session: AsyncSession = Depends(get_session)):
    pet = await session.get(PetInfo, pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")

    await session.delete(pet)
    await session.commit()
