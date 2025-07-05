# routes/maintenance.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from datetime import datetime, date

from ..database import get_session
from ..models import MaintenanceRequest, Resident, Unit
from ..schemas import MaintenanceRequestCreate, MaintenanceRequestUpdate, MaintenanceRequestOut

router = APIRouter(prefix="/maintenance", tags=["Maintenance Requests"])

@router.post("/", response_model=MaintenanceRequestOut, status_code=201)
async def create_maintenance_request(
    data: MaintenanceRequestCreate, 
    session: AsyncSession = Depends(get_session)
):
    """Create a new maintenance request"""
    try:
        # Verify unit exists
        unit = await session.get(Unit, data.unit_id)
        if not unit:
            raise HTTPException(status_code=404, detail="Unit not found")
        
        # Verify resident exists
        resident = await session.get(Resident, data.resident_id)
        if not resident:
            raise HTTPException(status_code=404, detail="Resident not found")
        
        new_request = MaintenanceRequest(**data.dict())
        session.add(new_request)
        await session.commit()
        await session.refresh(new_request)
        return new_request
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to create maintenance request: {str(e)}")

@router.get("/", response_model=List[MaintenanceRequestOut])
async def list_maintenance_requests(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    unit_id: Optional[int] = Query(None, description="Filter by unit ID"),
    resident_id: Optional[int] = Query(None, description="Filter by resident ID"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    status: Optional[str] = Query(None, description="Filter by status"),
    category: Optional[str] = Query(None, description="Filter by category"),
    assigned_to: Optional[str] = Query(None, description="Filter by assigned person"),
    session: AsyncSession = Depends(get_session)
):
    """Get all maintenance requests with optional filtering and pagination"""
    try:
        query = select(MaintenanceRequest)
        
        if unit_id:
            query = query.where(MaintenanceRequest.unit_id == unit_id)
        
        if resident_id:
            query = query.where(MaintenanceRequest.resident_id == resident_id)
        
        if priority:
            query = query.where(MaintenanceRequest.priority == priority)
        
        if status:
            query = query.where(MaintenanceRequest.status == status)
        
        if category:
            query = query.where(MaintenanceRequest.category == category)
        
        if assigned_to:
            query = query.where(MaintenanceRequest.assigned_to.ilike(f"%{assigned_to}%"))
        
        query = query.offset(skip).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch maintenance requests: {str(e)}")

@router.get("/{request_id}", response_model=MaintenanceRequestOut)
async def get_maintenance_request(
    request_id: int, 
    session: AsyncSession = Depends(get_session)
):
    """Get a specific maintenance request by ID"""
    try:
        request = await session.get(MaintenanceRequest, request_id)
        if not request:
            raise HTTPException(status_code=404, detail="Maintenance request not found")
        return request
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch maintenance request: {str(e)}")

@router.put("/{request_id}", response_model=MaintenanceRequestOut)
async def update_maintenance_request(
    request_id: int, 
    updates: MaintenanceRequestUpdate, 
    session: AsyncSession = Depends(get_session)
):
    """Update a maintenance request"""
    try:
        request = await session.get(MaintenanceRequest, request_id)
        if not request:
            raise HTTPException(status_code=404, detail="Maintenance request not found")
        
        update_data = updates.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(request, key, value)
        
        request.updated_at = datetime.utcnow()
        await session.commit()
        await session.refresh(request)
        return request
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to update maintenance request: {str(e)}")

@router.delete("/{request_id}", status_code=204)
async def delete_maintenance_request(
    request_id: int, 
    session: AsyncSession = Depends(get_session)
):
    """Delete a maintenance request"""
    try:
        request = await session.get(MaintenanceRequest, request_id)
        if not request:
            raise HTTPException(status_code=404, detail="Maintenance request not found")

        await session.delete(request)
        await session.commit()
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to delete maintenance request: {str(e)}")

@router.get("/unit/{unit_id}", response_model=List[MaintenanceRequestOut])
async def get_maintenance_requests_by_unit(
    unit_id: int,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    session: AsyncSession = Depends(get_session)
):
    """Get all maintenance requests for a specific unit"""
    try:
        # Verify unit exists
        unit = await session.get(Unit, unit_id)
        if not unit:
            raise HTTPException(status_code=404, detail="Unit not found")
        
        query = select(MaintenanceRequest).where(MaintenanceRequest.unit_id == unit_id).offset(skip).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch maintenance requests: {str(e)}")

@router.get("/resident/{resident_id}", response_model=List[MaintenanceRequestOut])
async def get_maintenance_requests_by_resident(
    resident_id: int,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    session: AsyncSession = Depends(get_session)
):
    """Get all maintenance requests for a specific resident"""
    try:
        # Verify resident exists
        resident = await session.get(Resident, resident_id)
        if not resident:
            raise HTTPException(status_code=404, detail="Resident not found")
        
        query = select(MaintenanceRequest).where(MaintenanceRequest.resident_id == resident_id).offset(skip).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch maintenance requests: {str(e)}")

@router.get("/stats/summary", response_model=dict)
async def get_maintenance_summary(
    session: AsyncSession = Depends(get_session)
):
    """Get maintenance request summary statistics"""
    try:
        # Get counts by status
        status_counts = await session.execute(
            select(
                MaintenanceRequest.status,
                func.count(MaintenanceRequest.id).label("count")
            ).group_by(MaintenanceRequest.status)
        )
        
        # Get counts by priority
        priority_counts = await session.execute(
            select(
                MaintenanceRequest.priority,
                func.count(MaintenanceRequest.id).label("count")
            ).group_by(MaintenanceRequest.priority)
        )
        
        # Get total cost
        total_cost = await session.execute(
            select(func.sum(MaintenanceRequest.actual_cost))
        )
        
        return {
            "status_counts": {row.status.value: row.count for row in status_counts},
            "priority_counts": {row.priority.value: row.count for row in priority_counts},
            "total_cost": float(total_cost.scalar() or 0),
            "total_requests": sum(row.count for row in status_counts)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch maintenance summary: {str(e)}") 