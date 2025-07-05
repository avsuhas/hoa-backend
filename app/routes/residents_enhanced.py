# routes/residents_enhanced.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from datetime import datetime, date
from uuid import UUID

from ..database import get_session
from ..models import ResidentEnhanced, User
from ..schemas import ResidentEnhancedCreate, ResidentEnhancedUpdate, ResidentEnhancedOut

router = APIRouter(prefix="/residents-enhanced", tags=["Enhanced Residents"])

@router.post("/", response_model=ResidentEnhancedOut, status_code=201)
async def create_resident(
    data: ResidentEnhancedCreate, 
    session: AsyncSession = Depends(get_session)
):
    """Create a new enhanced resident"""
    try:
        # Check if user_id is provided and exists
        if data.user_id:
            user = await session.get(User, data.user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
        
        new_resident = ResidentEnhanced(**data.dict())
        session.add(new_resident)
        await session.commit()
        await session.refresh(new_resident)
        return new_resident
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to create resident: {str(e)}")

@router.get("/", response_model=List[ResidentEnhancedOut])
async def list_residents(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    resident_type: Optional[str] = Query(None, description="Filter by resident type"),
    role: Optional[str] = Query(None, description="Filter by role"),
    unit_id: Optional[UUID] = Query(None, description="Filter by unit ID"),
    property_id: Optional[UUID] = Query(None, description="Filter by property ID"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    is_primary: Optional[bool] = Query(None, description="Filter by primary resident status"),
    search: Optional[str] = Query(None, description="Search by name or email"),
    session: AsyncSession = Depends(get_session)
):
    """Get all enhanced residents with optional filtering and pagination"""
    try:
        query = select(ResidentEnhanced)
        
        if resident_type:
            query = query.where(ResidentEnhanced.resident_type == resident_type)
        if role:
            query = query.where(ResidentEnhanced.role == role)
        if unit_id:
            query = query.where(ResidentEnhanced.unit_id == unit_id)
        if property_id:
            query = query.where(ResidentEnhanced.property_id == property_id)
        if is_active is not None:
            query = query.where(ResidentEnhanced.is_active == is_active)
        if is_primary is not None:
            query = query.where(ResidentEnhanced.is_primary == is_primary)
        if search:
            query = query.where(
                (ResidentEnhanced.first_name.ilike(f"%{search}%")) |
                (ResidentEnhanced.last_name.ilike(f"%{search}%")) |
                (ResidentEnhanced.email.ilike(f"%{search}%"))
            )
        
        query = query.offset(skip).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch residents: {str(e)}")

@router.get("/{resident_id}", response_model=ResidentEnhancedOut)
async def get_resident(
    resident_id: UUID, 
    session: AsyncSession = Depends(get_session)
):
    """Get a specific enhanced resident by ID"""
    try:
        resident = await session.get(ResidentEnhanced, resident_id)
        if not resident:
            raise HTTPException(status_code=404, detail="Resident not found")
        return resident
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch resident: {str(e)}")

@router.put("/{resident_id}", response_model=ResidentEnhancedOut)
async def update_resident(
    resident_id: UUID, 
    updates: ResidentEnhancedUpdate, 
    session: AsyncSession = Depends(get_session)
):
    """Update an enhanced resident"""
    try:
        resident = await session.get(ResidentEnhanced, resident_id)
        if not resident:
            raise HTTPException(status_code=404, detail="Resident not found")
        
        update_data = updates.dict(exclude_unset=True)
        
        # Check if user_id is being updated and if it exists
        if 'user_id' in update_data and update_data['user_id']:
            user = await session.get(User, update_data['user_id'])
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
        
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
    resident_id: UUID, 
    session: AsyncSession = Depends(get_session)
):
    """Delete an enhanced resident"""
    try:
        resident = await session.get(ResidentEnhanced, resident_id)
        if not resident:
            raise HTTPException(status_code=404, detail="Resident not found")

        await session.delete(resident)
        await session.commit()
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to delete resident: {str(e)}")

@router.get("/unit/{unit_id}", response_model=List[ResidentEnhancedOut])
async def get_residents_by_unit(
    unit_id: UUID,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    session: AsyncSession = Depends(get_session)
):
    """Get all residents for a specific unit"""
    try:
        query = select(ResidentEnhanced).where(ResidentEnhanced.unit_id == unit_id).offset(skip).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch residents: {str(e)}")

@router.get("/property/{property_id}", response_model=List[ResidentEnhancedOut])
async def get_residents_by_property(
    property_id: UUID,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    session: AsyncSession = Depends(get_session)
):
    """Get all residents for a specific property"""
    try:
        query = select(ResidentEnhanced).where(ResidentEnhanced.property_id == property_id).offset(skip).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch residents: {str(e)}")

@router.get("/user/{user_id}", response_model=List[ResidentEnhancedOut])
async def get_residents_by_user(
    user_id: UUID,
    session: AsyncSession = Depends(get_session)
):
    """Get all residents associated with a specific user"""
    try:
        user = await session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return user.residents
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch residents: {str(e)}")

@router.put("/{resident_id}/activate", response_model=ResidentEnhancedOut)
async def activate_resident(
    resident_id: UUID, 
    session: AsyncSession = Depends(get_session)
):
    """Activate a resident account"""
    try:
        resident = await session.get(ResidentEnhanced, resident_id)
        if not resident:
            raise HTTPException(status_code=404, detail="Resident not found")
        
        resident.is_active = True
        resident.updated_at = datetime.utcnow()
        await session.commit()
        await session.refresh(resident)
        return resident
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to activate resident: {str(e)}")

@router.put("/{resident_id}/deactivate", response_model=ResidentEnhancedOut)
async def deactivate_resident(
    resident_id: UUID, 
    session: AsyncSession = Depends(get_session)
):
    """Deactivate a resident account"""
    try:
        resident = await session.get(ResidentEnhanced, resident_id)
        if not resident:
            raise HTTPException(status_code=404, detail="Resident not found")
        
        resident.is_active = False
        resident.updated_at = datetime.utcnow()
        await session.commit()
        await session.refresh(resident)
        return resident
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to deactivate resident: {str(e)}")

@router.put("/{resident_id}/set-primary", response_model=ResidentEnhancedOut)
async def set_primary_resident(
    resident_id: UUID, 
    session: AsyncSession = Depends(get_session)
):
    """Set a resident as the primary resident for their unit"""
    try:
        resident = await session.get(ResidentEnhanced, resident_id)
        if not resident:
            raise HTTPException(status_code=404, detail="Resident not found")
        
        # Set all other residents in the same unit as non-primary
        await session.execute(
            select(ResidentEnhanced)
            .where(
                ResidentEnhanced.unit_id == resident.unit_id,
                ResidentEnhanced.id != resident_id
            )
        )
        
        # Set this resident as primary
        resident.is_primary = True
        resident.updated_at = datetime.utcnow()
        await session.commit()
        await session.refresh(resident)
        return resident
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to set primary resident: {str(e)}")

@router.get("/stats/summary", response_model=dict)
async def get_resident_summary(
    session: AsyncSession = Depends(get_session)
):
    """Get resident summary statistics"""
    try:
        # Get total count
        total_count = await session.scalar(select(func.count(ResidentEnhanced.id)))
        
        # Get active count
        active_count = await session.scalar(select(func.count(ResidentEnhanced.id)).where(ResidentEnhanced.is_active == True))
        
        # Get primary residents count
        primary_count = await session.scalar(select(func.count(ResidentEnhanced.id)).where(ResidentEnhanced.is_primary == True))
        
        # Get counts by resident type
        type_counts = {}
        types = ['owner', 'tenant', 'authorized_user']
        
        for resident_type in types:
            count = await session.scalar(
                select(func.count(ResidentEnhanced.id)).where(ResidentEnhanced.resident_type == resident_type)
            )
            type_counts[resident_type] = count or 0
        
        # Get counts by role
        role_counts = {}
        roles = ['super_admin', 'property_manager', 'board_member', 'community_admin', 'resident', 'tenant']
        
        for role in roles:
            count = await session.scalar(
                select(func.count(ResidentEnhanced.id)).where(ResidentEnhanced.role == role)
            )
            role_counts[role] = count or 0
        
        return {
            "total_residents": total_count or 0,
            "active_residents": active_count or 0,
            "primary_residents": primary_count or 0,
            "inactive_residents": (total_count or 0) - (active_count or 0),
            "resident_type_distribution": type_counts,
            "role_distribution": role_counts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch resident summary: {str(e)}")

@router.get("/{resident_id}/vehicles", response_model=dict)
async def get_resident_vehicles(
    resident_id: UUID,
    session: AsyncSession = Depends(get_session)
):
    """Get vehicle information for a specific resident"""
    try:
        resident = await session.get(ResidentEnhanced, resident_id)
        if not resident:
            raise HTTPException(status_code=404, detail="Resident not found")
        
        return {
            "resident_id": resident_id,
            "resident_name": f"{resident.first_name} {resident.last_name}",
            "vehicles": resident.vehicle_info
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch vehicle information: {str(e)}")

@router.get("/{resident_id}/pets", response_model=dict)
async def get_resident_pets(
    resident_id: UUID,
    session: AsyncSession = Depends(get_session)
):
    """Get pet information for a specific resident"""
    try:
        resident = await session.get(ResidentEnhanced, resident_id)
        if not resident:
            raise HTTPException(status_code=404, detail="Resident not found")
        
        return {
            "resident_id": resident_id,
            "resident_name": f"{resident.first_name} {resident.last_name}",
            "pets": resident.pet_info
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch pet information: {str(e)}")

@router.get("/{resident_id}/emergency-contact", response_model=dict)
async def get_resident_emergency_contact(
    resident_id: UUID,
    session: AsyncSession = Depends(get_session)
):
    """Get emergency contact information for a specific resident"""
    try:
        resident = await session.get(ResidentEnhanced, resident_id)
        if not resident:
            raise HTTPException(status_code=404, detail="Resident not found")
        
        return {
            "resident_id": resident_id,
            "resident_name": f"{resident.first_name} {resident.last_name}",
            "emergency_contact": resident.emergency_contact
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch emergency contact: {str(e)}") 