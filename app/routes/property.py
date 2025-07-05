# routes/property.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID

from ..database import get_session
from ..models import Property
from ..schemas import PropertyCreate, PropertyUpdate, PropertyOut

router = APIRouter(prefix="/properties", tags=["Properties"])

@router.post("/", response_model=PropertyOut)
async def create_property(data: PropertyCreate, session: AsyncSession = Depends(get_session)):
    new_property = Property(**data.dict())
    session.add(new_property)
    await session.commit()
    await session.refresh(new_property)
    return new_property

@router.get("/", response_model=List[PropertyOut])
async def list_properties(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Property))
    return result.scalars().all()

@router.get("/{property_id}", response_model=PropertyOut)
async def get_property(property_id: UUID, session: AsyncSession = Depends(get_session)):
    property = await session.get(Property, property_id)
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    return property

@router.put("/{property_id}", response_model=PropertyOut)
async def update_property(property_id: UUID, updates: PropertyUpdate, session: AsyncSession = Depends(get_session)):
    property = await session.get(Property, property_id)
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(property, key, value)

    await session.commit()
    await session.refresh(property)
    return property

@router.delete("/{property_id}", status_code=204)
async def delete_property(property_id: UUID, session: AsyncSession = Depends(get_session)):
    property = await session.get(Property, property_id)
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")

    await session.delete(property)
    await session.commit()
