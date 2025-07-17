# routes/contractors.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from datetime import datetime, date
from uuid import UUID

from ..database import get_session
from ..models import Contractor, User
from ..schemas import ContractorCreate, ContractorUpdate, ContractorOut
from ..auth import get_current_active_user, require_roles

router = APIRouter(prefix="/contractors", tags=["Contractors"])

@router.post("/", response_model=ContractorOut, status_code=201)
async def create_contractor(
    data: ContractorCreate, 
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_roles(["super_admin", "property_manager"]))
):
    """Create a new contractor"""
    try:
        new_contractor = Contractor(**data.dict())
        session.add(new_contractor)
        await session.commit()
        await session.refresh(new_contractor)
        return new_contractor
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to create contractor: {str(e)}")

@router.get("/", response_model=List[ContractorOut])
async def list_contractors(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    search: Optional[str] = Query(None, description="Search by name, company, or email"),
    specialty: Optional[str] = Query(None, description="Filter by specialty"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    min_rating: Optional[float] = Query(None, ge=0, le=5, description="Minimum rating filter"),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Get all contractors with optional filtering and pagination"""
    try:
        query = select(Contractor)
        
        if search:
            query = query.where(
                (Contractor.name.ilike(f"%{search}%")) | 
                (Contractor.company.ilike(f"%{search}%")) |
                (Contractor.email.ilike(f"%{search}%"))
            )
        
        if specialty:
            query = query.where(Contractor.specialties.contains([specialty]))
        
        if is_active is not None:
            query = query.where(Contractor.is_active == is_active)
        
        if min_rating is not None:
            query = query.where(Contractor.rating >= min_rating)
        
        query = query.offset(skip).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch contractors: {str(e)}")

@router.get("/{contractor_id}", response_model=ContractorOut)
async def get_contractor(
    contractor_id: UUID, 
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific contractor by ID"""
    try:
        contractor = await session.get(Contractor, contractor_id)
        if not contractor:
            raise HTTPException(status_code=404, detail="Contractor not found")
        return contractor
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch contractor: {str(e)}")

@router.put("/{contractor_id}", response_model=ContractorOut)
async def update_contractor(
    contractor_id: UUID, 
    updates: ContractorUpdate, 
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_roles(["super_admin", "property_manager"]))
):
    """Update a contractor"""
    try:
        contractor = await session.get(Contractor, contractor_id)
        if not contractor:
            raise HTTPException(status_code=404, detail="Contractor not found")
        
        update_data = updates.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(contractor, key, value)
        
        contractor.updated_at = datetime.utcnow()
        await session.commit()
        await session.refresh(contractor)
        return contractor
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to update contractor: {str(e)}")

@router.delete("/{contractor_id}", status_code=204)
async def delete_contractor(
    contractor_id: UUID, 
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_roles(["super_admin", "property_manager"]))
):
    """Delete a contractor"""
    try:
        contractor = await session.get(Contractor, contractor_id)
        if not contractor:
            raise HTTPException(status_code=404, detail="Contractor not found")

        await session.delete(contractor)
        await session.commit()
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to delete contractor: {str(e)}")

@router.get("/specialty/{specialty}", response_model=List[ContractorOut])
async def get_contractors_by_specialty(
    specialty: str,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Get all contractors with a specific specialty"""
    try:
        query = select(Contractor).where(Contractor.specialties.contains([specialty])).offset(skip).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch contractors: {str(e)}")

@router.get("/stats/summary", response_model=dict)
async def get_contractor_summary(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_roles(["super_admin", "property_manager", "board_member"]))
):
    """Get contractor summary statistics"""
    try:
        # Get total count
        total_count = await session.scalar(select(func.count(Contractor.id)))
        
        # Get active count
        active_count = await session.scalar(select(func.count(Contractor.id)).where(Contractor.is_active == True))
        
        # Get average rating
        avg_rating = await session.scalar(select(func.avg(Contractor.rating)))
        
        # Get count by rating range
        high_rated = await session.scalar(
            select(func.count(Contractor.id)).where(Contractor.rating >= 4.0)
        )
        
        return {
            "total_contractors": total_count or 0,
            "active_contractors": active_count or 0,
            "average_rating": float(avg_rating or 0),
            "high_rated_contractors": high_rated or 0,
            "inactive_contractors": (total_count or 0) - (active_count or 0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch contractor summary: {str(e)}")

@router.get("/{contractor_id}/maintenance-requests", response_model=dict)
async def get_contractor_maintenance_requests(
    contractor_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_roles(["super_admin", "property_manager", "board_member"]))
):
    """Get maintenance requests assigned to a specific contractor"""
    try:
        contractor = await session.get(Contractor, contractor_id)
        if not contractor:
            raise HTTPException(status_code=404, detail="Contractor not found")
        
        # This would need to be implemented when we have the maintenance requests relationship
        # For now, return basic contractor info
        return {
            "contractor_id": contractor_id,
            "contractor_name": contractor.name,
            "maintenance_requests_count": len(contractor.maintenance_requests) if contractor.maintenance_requests else 0
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch contractor maintenance requests: {str(e)}") 