# routes/vehicle_info.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from ..database import get_session
from ..models import VehicleInfo
from ..schemas import VehicleInfoCreate, VehicleInfoUpdate, VehicleInfoOut

router = APIRouter(prefix="/vehicles", tags=["Vehicles Info"])

@router.post("/", response_model=VehicleInfoOut)
async def create_vehicle(vehicle: VehicleInfoCreate, session: AsyncSession = Depends(get_session)):
    new_vehicle = VehicleInfo(**vehicle.dict())
    session.add(new_vehicle)
    await session.commit()
    await session.refresh(new_vehicle)
    return new_vehicle

@router.get("/", response_model=List[VehicleInfoOut])
async def list_vehicles(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(VehicleInfo))
    return result.scalars().all()

@router.get("/{vehicle_id}", response_model=VehicleInfoOut)
async def get_vehicle(vehicle_id: int, session: AsyncSession = Depends(get_session)):
    vehicle = await session.get(VehicleInfo, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle

@router.put("/{vehicle_id}", response_model=VehicleInfoOut)
async def update_vehicle(vehicle_id: int, updates: VehicleInfoUpdate, session: AsyncSession = Depends(get_session)):
    vehicle = await session.get(VehicleInfo, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    for key, value in updates.dict(exclude_unset=True).items():
        setattr(vehicle, key, value)

    await session.commit()
    await session.refresh(vehicle)
    return vehicle

@router.delete("/{vehicle_id}", status_code=204)
async def delete_vehicle(vehicle_id: int, session: AsyncSession = Depends(get_session)):
    vehicle = await session.get(VehicleInfo, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    await session.delete(vehicle)
    await session.commit()
