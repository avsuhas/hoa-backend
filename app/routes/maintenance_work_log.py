# routes/maintenance_work_log.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID

from ..database import get_session
from ..models import MaintenanceWorkLog
from ..schemas import MaintenanceWorkLogCreate, MaintenanceWorkLogUpdate, MaintenanceWorkLogOut

router = APIRouter(prefix="/maintenance-work-logs", tags=["Maintenance Work Logs"])

@router.post("/", response_model=MaintenanceWorkLogOut)
async def create_work_log(log: MaintenanceWorkLogCreate, session: AsyncSession = Depends(get_session)):
    new_log = MaintenanceWorkLog(**log.dict())
    session.add(new_log)
    await session.commit()
    await session.refresh(new_log)
    return new_log

@router.get("/", response_model=List[MaintenanceWorkLogOut])
async def list_work_logs(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(MaintenanceWorkLog))
    return result.scalars().all()

@router.get("/{log_id}", response_model=MaintenanceWorkLogOut)
async def get_work_log(log_id: UUID, session: AsyncSession = Depends(get_session)):
    log = await session.get(MaintenanceWorkLog, log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Work log not found")
    return log

@router.put("/{log_id}", response_model=MaintenanceWorkLogOut)
async def update_work_log(log_id: UUID, updates: MaintenanceWorkLogUpdate, session: AsyncSession = Depends(get_session)):
    log = await session.get(MaintenanceWorkLog, log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Work log not found")
    
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(log, key, value)

    await session.commit()
    await session.refresh(log)
    return log

@router.delete("/{log_id}", status_code=204)
async def delete_work_log(log_id: UUID, session: AsyncSession = Depends(get_session)):
    log = await session.get(MaintenanceWorkLog, log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Work log not found")

    await session.delete(log)
    await session.commit()
