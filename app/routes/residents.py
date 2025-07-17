# routes/residents.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from datetime import datetime

from ..database import get_session
from ..models import Resident, Unit, User
from ..schemas import ResidentCreate, ResidentUpdate, ResidentOut
from ..auth import get_current_active_user, require_roles

router = APIRouter(prefix="/residents", tags=["Residents"])

@router.post("/", response_model=ResidentOut, status_code=201)
async def create_resident(
    data: ResidentCreate, 
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_roles(["super_admin", "property_manager", "board_member"]))
):
    """Create a new resident"""
    try:
        # Verify unit exists
        unit = await session.get(Unit, data.unit_id)
        if not unit:
            raise HTTPException(status_code=404, detail="Unit not found")
        
        new_resident = Resident(**data.dict())
        session.add(new_resident)
        await session.commit()
        await session.refresh(new_resident)
        return new_resident
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to create resident: {str(e)}")

@router.get("/", response_model=List[ResidentOut])
async def list_residents(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    unit_id: Optional[int] = Query(None, description="Filter by unit ID"),
    resident_type: Optional[str] = Query(None, description="Filter by resident type"),
    search: Optional[str] = Query(None, description="Search by name or email"),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Get all residents with optional filtering and pagination"""
    try:
        query = select(Resident)
        
        if unit_id:
            query = query.where(Resident.unit_id == unit_id)
        
        if resident_type:
            query = query.where(Resident.resident_type == resident_type)
        
        if search:
            query = query.where(
                (Resident.first_name.ilike(f"%{search}%")) | 
                (Resident.last_name.ilike(f"%{search}%")) |
                (Resident.email.ilike(f"%{search}%"))
            )
        
        query = query.offset(skip).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch residents: {str(e)}")

@router.get("/{resident_id}", response_model=ResidentOut)
async def get_resident(
    resident_id: int, 
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific resident by ID"""
    try:
        resident = await session.get(Resident, resident_id)
        if not resident:
            raise HTTPException(status_code=404, detail="Resident not found")
        return resident
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch resident: {str(e)}")

@router.put("/{resident_id}", response_model=ResidentOut)
async def update_resident(
    resident_id: int, 
    updates: ResidentUpdate, 
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_roles(["super_admin", "property_manager", "board_member"]))
):
    """Update a resident"""
    try:
        resident = await session.get(Resident, resident_id)
        if not resident:
            raise HTTPException(status_code=404, detail="Resident not found")
        
        update_data = updates.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(resident, key, value)
        
        resident.updated_at = datetime.utcnow()
        await session.commit()
        await session.refresh(resident)
        return resident
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to update resident: {str(e)}")

@router.delete("/{resident_id}", status_code=204)
async def delete_resident(
    resident_id: int, 
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_roles(["super_admin", "property_manager"]))
):
    """Delete a resident"""
    try:
        resident = await session.get(Resident, resident_id)
        if not resident:
            raise HTTPException(status_code=404, detail="Resident not found")

        await session.delete(resident)
        await session.commit()
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to delete resident: {str(e)}")

@router.get("/unit/{unit_id}", response_model=List[ResidentOut])
async def get_residents_by_unit(
    unit_id: int,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Get all residents for a specific unit"""
    try:
        # Verify unit exists
        unit = await session.get(Unit, unit_id)
        if not unit:
            raise HTTPException(status_code=404, detail="Unit not found")
        
        query = select(Resident).where(Resident.unit_id == unit_id).offset(skip).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch residents: {str(e)}")

@router.get("/{resident_id}/stats", response_model=dict)
async def get_resident_stats(
    resident_id: int, 
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Get resident statistics"""
    try:
        resident = await session.get(Resident, resident_id)
        if not resident:
            raise HTTPException(status_code=404, detail="Resident not found")
        
        # Get payment count for this resident
        payment_count_query = select(func.count()).select_from(Resident).where(Resident.id == resident_id)
        payment_count = await session.scalar(payment_count_query)
        
        return {
            "resident_id": resident_id,
            "full_name": f"{resident.first_name} {resident.last_name}",
            "resident_type": resident.resident_type.value,
            "unit_id": resident.unit_id,
            "payment_count": payment_count or 0,
            "has_emergency_contact": bool(resident.emergency_contact_name and resident.emergency_contact_phone)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch resident stats: {str(e)}") 