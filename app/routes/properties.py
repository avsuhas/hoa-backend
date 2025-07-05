# routes/properties.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from datetime import datetime

from ..database import get_session
from ..models import Property
from ..schemas import PropertyCreate, PropertyUpdate, PropertyOut

router = APIRouter(prefix="/properties", tags=["Properties"])

@router.post("/", response_model=PropertyOut, status_code=201)
async def create_property(
    data: PropertyCreate, 
    session: AsyncSession = Depends(get_session)
):
    """Create a new property"""
    try:
        new_property = Property(**data.dict())
        session.add(new_property)
        await session.commit()
        await session.refresh(new_property)
        return new_property
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to create property: {str(e)}")

@router.get("/", response_model=List[PropertyOut])
async def list_properties(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    search: Optional[str] = Query(None, description="Search by property name or address"),
    property_type: Optional[str] = Query(None, description="Filter by property type"),
    session: AsyncSession = Depends(get_session)
):
    """Get all properties with optional filtering and pagination"""
    try:
        query = select(Property)
        
        if search:
            query = query.where(
                (Property.name.ilike(f"%{search}%")) | 
                (Property.address.ilike(f"%{search}%"))
            )
        
        if property_type:
            query = query.where(Property.property_type == property_type)
        
        query = query.offset(skip).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch properties: {str(e)}")

@router.get("/{property_id}", response_model=PropertyOut)
async def get_property(
    property_id: int, 
    session: AsyncSession = Depends(get_session)
):
    """Get a specific property by ID"""
    try:
        property = await session.get(Property, property_id)
        if not property:
            raise HTTPException(status_code=404, detail="Property not found")
        return property
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch property: {str(e)}")

@router.put("/{property_id}", response_model=PropertyOut)
async def update_property(
    property_id: int, 
    updates: PropertyUpdate, 
    session: AsyncSession = Depends(get_session)
):
    """Update a property"""
    try:
        property = await session.get(Property, property_id)
        if not property:
            raise HTTPException(status_code=404, detail="Property not found")
        
        update_data = updates.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(property, key, value)
        
        property.updated_at = datetime.utcnow()
        await session.commit()
        await session.refresh(property)
        return property
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to update property: {str(e)}")

@router.delete("/{property_id}", status_code=204)
async def delete_property(
    property_id: int, 
    session: AsyncSession = Depends(get_session)
):
    """Delete a property"""
    try:
        property = await session.get(Property, property_id)
        if not property:
            raise HTTPException(status_code=404, detail="Property not found")

        await session.delete(property)
        await session.commit()
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to delete property: {str(e)}")

@router.get("/{property_id}/stats", response_model=dict)
async def get_property_stats(
    property_id: int, 
    session: AsyncSession = Depends(get_session)
):
    """Get property statistics"""
    try:
        property = await session.get(Property, property_id)
        if not property:
            raise HTTPException(status_code=404, detail="Property not found")
        
        # Get unit count for this property
        unit_count_query = select(func.count()).select_from(Property).where(Property.id == property_id)
        unit_count = await session.scalar(unit_count_query)
        
        return {
            "property_id": property_id,
            "total_units": property.total_units,
            "occupied_units": unit_count or 0,
            "vacancy_rate": ((property.total_units - (unit_count or 0)) / property.total_units * 100) if property.total_units > 0 else 0
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch property stats: {str(e)}") 