# routes/maintenance_enhanced.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import List, Optional
from datetime import datetime, date
from uuid import UUID

from ..database import get_session
from ..models import MaintenanceRequestEnhanced, MaintenanceWorkLog, Contractor
from ..schemas import (
    MaintenanceRequestEnhancedCreate, 
    MaintenanceRequestEnhancedUpdate, 
    MaintenanceRequestEnhancedOut,
    MaintenanceWorkLogCreate,
    MaintenanceWorkLogUpdate,
    MaintenanceWorkLogOut
)

router = APIRouter(prefix="/maintenance-enhanced", tags=["Enhanced Maintenance"])

# Enhanced Maintenance Request Routes
@router.post("/requests/", response_model=MaintenanceRequestEnhancedOut, status_code=201)
async def create_maintenance_request(
    data: MaintenanceRequestEnhancedCreate, 
    session: AsyncSession = Depends(get_session)
):
    """Create a new enhanced maintenance request"""
    try:
        new_request = MaintenanceRequestEnhanced(**data.dict())
        session.add(new_request)
        await session.commit()
        await session.refresh(new_request)
        return new_request
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to create maintenance request: {str(e)}")

@router.get("/requests/", response_model=List[MaintenanceRequestEnhancedOut])
async def list_maintenance_requests(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    status: Optional[str] = Query(None, description="Filter by status"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    category: Optional[str] = Query(None, description="Filter by category"),
    unit_id: Optional[UUID] = Query(None, description="Filter by unit ID"),
    property_id: Optional[UUID] = Query(None, description="Filter by property ID"),
    resident_id: Optional[UUID] = Query(None, description="Filter by resident ID"),
    contractor_id: Optional[UUID] = Query(None, description="Filter by contractor ID"),
    is_emergency: Optional[bool] = Query(None, description="Filter by emergency status"),
    search: Optional[str] = Query(None, description="Search in title and description"),
    session: AsyncSession = Depends(get_session)
):
    """Get all enhanced maintenance requests with filtering and pagination"""
    try:
        query = select(MaintenanceRequestEnhanced)
        
        if status:
            query = query.where(MaintenanceRequestEnhanced.status == status)
        if priority:
            query = query.where(MaintenanceRequestEnhanced.priority == priority)
        if category:
            query = query.where(MaintenanceRequestEnhanced.category == category)
        if unit_id:
            query = query.where(MaintenanceRequestEnhanced.unit_id == unit_id)
        if property_id:
            query = query.where(MaintenanceRequestEnhanced.property_id == property_id)
        if resident_id:
            query = query.where(MaintenanceRequestEnhanced.resident_id == resident_id)
        if contractor_id:
            query = query.where(MaintenanceRequestEnhanced.contractor_id == contractor_id)
        if is_emergency is not None:
            query = query.where(MaintenanceRequestEnhanced.is_emergency == is_emergency)
        if search:
            query = query.where(
                (MaintenanceRequestEnhanced.title.ilike(f"%{search}%")) |
                (MaintenanceRequestEnhanced.description.ilike(f"%{search}%"))
            )
        
        query = query.offset(skip).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch maintenance requests: {str(e)}")

@router.get("/requests/{request_id}", response_model=MaintenanceRequestEnhancedOut)
async def get_maintenance_request(
    request_id: UUID, 
    session: AsyncSession = Depends(get_session)
):
    """Get a specific enhanced maintenance request by ID"""
    try:
        request = await session.get(MaintenanceRequestEnhanced, request_id)
        if not request:
            raise HTTPException(status_code=404, detail="Maintenance request not found")
        return request
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch maintenance request: {str(e)}")

@router.put("/requests/{request_id}", response_model=MaintenanceRequestEnhancedOut)
async def update_maintenance_request(
    request_id: UUID, 
    updates: MaintenanceRequestEnhancedUpdate, 
    session: AsyncSession = Depends(get_session)
):
    """Update an enhanced maintenance request"""
    try:
        request = await session.get(MaintenanceRequestEnhanced, request_id)
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

@router.delete("/requests/{request_id}", status_code=204)
async def delete_maintenance_request(
    request_id: UUID, 
    session: AsyncSession = Depends(get_session)
):
    """Delete an enhanced maintenance request"""
    try:
        request = await session.get(MaintenanceRequestEnhanced, request_id)
        if not request:
            raise HTTPException(status_code=404, detail="Maintenance request not found")

        await session.delete(request)
        await session.commit()
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to delete maintenance request: {str(e)}")

@router.get("/requests/{request_id}/work-logs", response_model=List[MaintenanceWorkLogOut])
async def get_maintenance_work_logs(
    request_id: UUID,
    session: AsyncSession = Depends(get_session)
):
    """Get all work logs for a specific maintenance request"""
    try:
        request = await session.get(MaintenanceRequestEnhanced, request_id)
        if not request:
            raise HTTPException(status_code=404, detail="Maintenance request not found")
        
        return request.work_logs
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch work logs: {str(e)}")

@router.get("/stats/summary", response_model=dict)
async def get_maintenance_summary(
    session: AsyncSession = Depends(get_session)
):
    """Get maintenance request summary statistics"""
    try:
        # Get total count
        total_count = await session.scalar(select(func.count(MaintenanceRequestEnhanced.id)))
        
        # Get counts by status
        pending_count = await session.scalar(
            select(func.count(MaintenanceRequestEnhanced.id))
            .where(MaintenanceRequestEnhanced.status == "pending")
        )
        
        in_progress_count = await session.scalar(
            select(func.count(MaintenanceRequestEnhanced.id))
            .where(MaintenanceRequestEnhanced.status == "in_progress")
        )
        
        completed_count = await session.scalar(
            select(func.count(MaintenanceRequestEnhanced.id))
            .where(MaintenanceRequestEnhanced.status == "completed")
        )
        
        emergency_count = await session.scalar(
            select(func.count(MaintenanceRequestEnhanced.id))
            .where(MaintenanceRequestEnhanced.is_emergency == True)
        )
        
        # Get average estimated cost
        avg_estimated_cost = await session.scalar(
            select(func.avg(MaintenanceRequestEnhanced.estimated_cost))
            .where(MaintenanceRequestEnhanced.estimated_cost.isnot(None))
        )
        
        return {
            "total_requests": total_count or 0,
            "pending_requests": pending_count or 0,
            "in_progress_requests": in_progress_count or 0,
            "completed_requests": completed_count or 0,
            "emergency_requests": emergency_count or 0,
            "average_estimated_cost": float(avg_estimated_cost or 0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch maintenance summary: {str(e)}")

# Maintenance Work Log Routes
@router.post("/work-logs/", response_model=MaintenanceWorkLogOut, status_code=201)
async def create_work_log(
    data: MaintenanceWorkLogCreate, 
    session: AsyncSession = Depends(get_session)
):
    """Create a new maintenance work log"""
    try:
        # Verify maintenance request exists
        request = await session.get(MaintenanceRequestEnhanced, data.maintenance_request_id)
        if not request:
            raise HTTPException(status_code=404, detail="Maintenance request not found")
        
        new_work_log = MaintenanceWorkLog(**data.dict())
        session.add(new_work_log)
        await session.commit()
        await session.refresh(new_work_log)
        return new_work_log
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to create work log: {str(e)}")

@router.get("/work-logs/", response_model=List[MaintenanceWorkLogOut])
async def list_work_logs(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    maintenance_request_id: Optional[UUID] = Query(None, description="Filter by maintenance request ID"),
    worker_name: Optional[str] = Query(None, description="Filter by worker name"),
    work_date: Optional[date] = Query(None, description="Filter by work date"),
    session: AsyncSession = Depends(get_session)
):
    """Get all maintenance work logs with filtering and pagination"""
    try:
        query = select(MaintenanceWorkLog)
        
        if maintenance_request_id:
            query = query.where(MaintenanceWorkLog.maintenance_request_id == maintenance_request_id)
        if worker_name:
            query = query.where(MaintenanceWorkLog.worker_name.ilike(f"%{worker_name}%"))
        if work_date:
            query = query.where(MaintenanceWorkLog.work_date == work_date)
        
        query = query.offset(skip).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch work logs: {str(e)}")

@router.get("/work-logs/{work_log_id}", response_model=MaintenanceWorkLogOut)
async def get_work_log(
    work_log_id: UUID, 
    session: AsyncSession = Depends(get_session)
):
    """Get a specific maintenance work log by ID"""
    try:
        work_log = await session.get(MaintenanceWorkLog, work_log_id)
        if not work_log:
            raise HTTPException(status_code=404, detail="Work log not found")
        return work_log
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch work log: {str(e)}")

@router.put("/work-logs/{work_log_id}", response_model=MaintenanceWorkLogOut)
async def update_work_log(
    work_log_id: UUID, 
    updates: MaintenanceWorkLogUpdate, 
    session: AsyncSession = Depends(get_session)
):
    """Update a maintenance work log"""
    try:
        work_log = await session.get(MaintenanceWorkLog, work_log_id)
        if not work_log:
            raise HTTPException(status_code=404, detail="Work log not found")
        
        update_data = updates.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(work_log, key, value)
        
        await session.commit()
        await session.refresh(work_log)
        return work_log
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to update work log: {str(e)}")

@router.delete("/work-logs/{work_log_id}", status_code=204)
async def delete_work_log(
    work_log_id: UUID, 
    session: AsyncSession = Depends(get_session)
):
    """Delete a maintenance work log"""
    try:
        work_log = await session.get(MaintenanceWorkLog, work_log_id)
        if not work_log:
            raise HTTPException(status_code=404, detail="Work log not found")

        await session.delete(work_log)
        await session.commit()
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to delete work log: {str(e)}")

@router.get("/work-logs/stats/summary", response_model=dict)
async def get_work_log_summary(
    session: AsyncSession = Depends(get_session)
):
    """Get work log summary statistics"""
    try:
        # Get total count
        total_count = await session.scalar(select(func.count(MaintenanceWorkLog.id)))
        
        # Get total hours worked
        total_hours = await session.scalar(select(func.sum(MaintenanceWorkLog.hours_worked)))
        
        # Get total cost
        total_cost = await session.scalar(select(func.sum(MaintenanceWorkLog.cost)))
        
        # Get average hours per work log
        avg_hours = await session.scalar(select(func.avg(MaintenanceWorkLog.hours_worked)))
        
        return {
            "total_work_logs": total_count or 0,
            "total_hours_worked": float(total_hours or 0),
            "total_cost": float(total_cost or 0),
            "average_hours_per_log": float(avg_hours or 0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch work log summary: {str(e)}") 