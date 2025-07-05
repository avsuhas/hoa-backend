# routes/violations.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from datetime import datetime, date

from ..database import get_session
from ..models import Violation, Resident, Unit
from ..schemas import ViolationCreate, ViolationUpdate, ViolationOut

router = APIRouter(prefix="/violations", tags=["Violations"])

@router.post("/", response_model=ViolationOut, status_code=201)
async def create_violation(
    data: ViolationCreate, 
    session: AsyncSession = Depends(get_session)
):
    """Create a new violation"""
    try:
        # Verify unit exists
        unit = await session.get(Unit, data.unit_id)
        if not unit:
            raise HTTPException(status_code=404, detail="Unit not found")
        
        # Verify resident exists
        resident = await session.get(Resident, data.resident_id)
        if not resident:
            raise HTTPException(status_code=404, detail="Resident not found")
        
        new_violation = Violation(**data.dict())
        session.add(new_violation)
        await session.commit()
        await session.refresh(new_violation)
        return new_violation
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to create violation: {str(e)}")

@router.get("/", response_model=List[ViolationOut])
async def list_violations(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    unit_id: Optional[int] = Query(None, description="Filter by unit ID"),
    resident_id: Optional[int] = Query(None, description="Filter by resident ID"),
    severity: Optional[str] = Query(None, description="Filter by severity"),
    status: Optional[str] = Query(None, description="Filter by status"),
    violation_type: Optional[str] = Query(None, description="Filter by violation type"),
    session: AsyncSession = Depends(get_session)
):
    """Get all violations with optional filtering and pagination"""
    try:
        query = select(Violation)
        
        if unit_id:
            query = query.where(Violation.unit_id == unit_id)
        
        if resident_id:
            query = query.where(Violation.resident_id == resident_id)
        
        if severity:
            query = query.where(Violation.severity == severity)
        
        if status:
            query = query.where(Violation.status == status)
        
        if violation_type:
            query = query.where(Violation.violation_type.ilike(f"%{violation_type}%"))
        
        query = query.offset(skip).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch violations: {str(e)}")

@router.get("/{violation_id}", response_model=ViolationOut)
async def get_violation(
    violation_id: int, 
    session: AsyncSession = Depends(get_session)
):
    """Get a specific violation by ID"""
    try:
        violation = await session.get(Violation, violation_id)
        if not violation:
            raise HTTPException(status_code=404, detail="Violation not found")
        return violation
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch violation: {str(e)}")

@router.put("/{violation_id}", response_model=ViolationOut)
async def update_violation(
    violation_id: int, 
    updates: ViolationUpdate, 
    session: AsyncSession = Depends(get_session)
):
    """Update a violation"""
    try:
        violation = await session.get(Violation, violation_id)
        if not violation:
            raise HTTPException(status_code=404, detail="Violation not found")
        
        update_data = updates.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(violation, key, value)
        
        violation.updated_at = datetime.utcnow()
        await session.commit()
        await session.refresh(violation)
        return violation
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to update violation: {str(e)}")

@router.delete("/{violation_id}", status_code=204)
async def delete_violation(
    violation_id: int, 
    session: AsyncSession = Depends(get_session)
):
    """Delete a violation"""
    try:
        violation = await session.get(Violation, violation_id)
        if not violation:
            raise HTTPException(status_code=404, detail="Violation not found")

        await session.delete(violation)
        await session.commit()
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to delete violation: {str(e)}")

@router.get("/unit/{unit_id}", response_model=List[ViolationOut])
async def get_violations_by_unit(
    unit_id: int,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    session: AsyncSession = Depends(get_session)
):
    """Get all violations for a specific unit"""
    try:
        # Verify unit exists
        unit = await session.get(Unit, unit_id)
        if not unit:
            raise HTTPException(status_code=404, detail="Unit not found")
        
        query = select(Violation).where(Violation.unit_id == unit_id).offset(skip).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch violations: {str(e)}")

@router.get("/resident/{resident_id}", response_model=List[ViolationOut])
async def get_violations_by_resident(
    resident_id: int,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    session: AsyncSession = Depends(get_session)
):
    """Get all violations for a specific resident"""
    try:
        # Verify resident exists
        resident = await session.get(Resident, resident_id)
        if not resident:
            raise HTTPException(status_code=404, detail="Resident not found")
        
        query = select(Violation).where(Violation.resident_id == resident_id).offset(skip).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch violations: {str(e)}")

@router.get("/stats/summary", response_model=dict)
async def get_violation_summary(
    session: AsyncSession = Depends(get_session)
):
    """Get violation summary statistics"""
    try:
        # Get counts by status
        status_counts = await session.execute(
            select(
                Violation.status,
                func.count(Violation.id).label("count")
            ).group_by(Violation.status)
        )
        
        # Get counts by severity
        severity_counts = await session.execute(
            select(
                Violation.severity,
                func.count(Violation.id).label("count")
            ).group_by(Violation.severity)
        )
        
        # Get total fines
        total_fines = await session.execute(
            select(func.sum(Violation.fine_amount))
        )
        
        return {
            "status_counts": {row.status.value: row.count for row in status_counts},
            "severity_counts": {row.severity.value: row.count for row in severity_counts},
            "total_fines": float(total_fines.scalar() or 0),
            "total_violations": sum(row.count for row in status_counts)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch violation summary: {str(e)}") 