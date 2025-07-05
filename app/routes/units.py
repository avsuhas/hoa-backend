# routes/units.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from datetime import datetime

from ..database import get_session
from ..models import Unit, Property
from ..schemas import UnitCreate, UnitUpdate, UnitOut

router = APIRouter(prefix="/units", tags=["Units"])

@router.post("/", response_model=UnitOut, status_code=201)
async def create_unit(
    data: UnitCreate, 
    session: AsyncSession = Depends(get_session)
):
    """Create a new unit"""
    try:
        # Verify property exists
        property = await session.get(Property, data.property_id)
        if not property:
            raise HTTPException(status_code=404, detail="Property not found")
        
        new_unit = Unit(**data.dict())
        session.add(new_unit)
        await session.commit()
        await session.refresh(new_unit)
        return new_unit
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to create unit: {str(e)}")

@router.get("/", response_model=List[UnitOut])
async def list_units(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    property_id: Optional[int] = Query(None, description="Filter by property ID"),
    unit_type: Optional[str] = Query(None, description="Filter by unit type"),
    search: Optional[str] = Query(None, description="Search by unit number"),
    session: AsyncSession = Depends(get_session)
):
    """Get all units with optional filtering and pagination"""
    try:
        query = select(Unit)
        
        if property_id:
            query = query.where(Unit.property_id == property_id)
        
        if unit_type:
            query = query.where(Unit.unit_type == unit_type)
        
        if search:
            query = query.where(Unit.unit_number.ilike(f"%{search}%"))
        
        query = query.offset(skip).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch units: {str(e)}")

@router.get("/{unit_id}", response_model=UnitOut)
async def get_unit(
    unit_id: int, 
    session: AsyncSession = Depends(get_session)
):
    """Get a specific unit by ID"""
    try:
        unit = await session.get(Unit, unit_id)
        if not unit:
            raise HTTPException(status_code=404, detail="Unit not found")
        return unit
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch unit: {str(e)}")

@router.put("/{unit_id}", response_model=UnitOut)
async def update_unit(
    unit_id: int, 
    updates: UnitUpdate, 
    session: AsyncSession = Depends(get_session)
):
    """Update a unit"""
    try:
        unit = await session.get(Unit, unit_id)
        if not unit:
            raise HTTPException(status_code=404, detail="Unit not found")
        
        update_data = updates.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(unit, key, value)
        
        unit.updated_at = datetime.utcnow()
        await session.commit()
        await session.refresh(unit)
        return unit
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to update unit: {str(e)}")

@router.delete("/{unit_id}", status_code=204)
async def delete_unit(
    unit_id: int, 
    session: AsyncSession = Depends(get_session)
):
    """Delete a unit"""
    try:
        unit = await session.get(Unit, unit_id)
        if not unit:
            raise HTTPException(status_code=404, detail="Unit not found")

        await session.delete(unit)
        await session.commit()
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to delete unit: {str(e)}")

@router.get("/property/{property_id}", response_model=List[UnitOut])
async def get_units_by_property(
    property_id: int,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    session: AsyncSession = Depends(get_session)
):
    """Get all units for a specific property"""
    try:
        # Verify property exists
        property = await session.get(Property, property_id)
        if not property:
            raise HTTPException(status_code=404, detail="Property not found")
        
        query = select(Unit).where(Unit.property_id == property_id).offset(skip).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch units: {str(e)}")

@router.get("/{unit_id}/stats", response_model=dict)
async def get_unit_stats(
    unit_id: int, 
    session: AsyncSession = Depends(get_session)
):
    """Get unit statistics"""
    try:
        unit = await session.get(Unit, unit_id)
        if not unit:
            raise HTTPException(status_code=404, detail="Unit not found")
        
        # Get resident count for this unit
        resident_count_query = select(func.count()).select_from(Unit).where(Unit.id == unit_id)
        resident_count = await session.scalar(resident_count_query)
        
        return {
            "unit_id": unit_id,
            "unit_number": unit.unit_number,
            "monthly_fee": float(unit.monthly_fee),
            "resident_count": resident_count or 0,
            "is_occupied": (resident_count or 0) > 0
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch unit stats: {str(e)}") 