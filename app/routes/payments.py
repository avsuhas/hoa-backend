# routes/payments.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from datetime import datetime, date

from ..database import get_session
from ..models import Payment, Resident, Unit
from ..schemas import PaymentCreate, PaymentUpdate, PaymentOut

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/", response_model=PaymentOut, status_code=201)
async def create_payment(
    data: PaymentCreate, 
    session: AsyncSession = Depends(get_session)
):
    """Create a new payment"""
    try:
        # Verify resident exists
        resident = await session.get(Resident, data.resident_id)
        if not resident:
            raise HTTPException(status_code=404, detail="Resident not found")
        
        # Verify unit exists
        unit = await session.get(Unit, data.unit_id)
        if not unit:
            raise HTTPException(status_code=404, detail="Unit not found")
        
        new_payment = Payment(**data.dict())
        session.add(new_payment)
        await session.commit()
        await session.refresh(new_payment)
        return new_payment
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to create payment: {str(e)}")

@router.get("/", response_model=List[PaymentOut])
async def list_payments(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    resident_id: Optional[int] = Query(None, description="Filter by resident ID"),
    unit_id: Optional[int] = Query(None, description="Filter by unit ID"),
    payment_type: Optional[str] = Query(None, description="Filter by payment type"),
    status: Optional[str] = Query(None, description="Filter by payment status"),
    start_date: Optional[date] = Query(None, description="Filter by start date"),
    end_date: Optional[date] = Query(None, description="Filter by end date"),
    session: AsyncSession = Depends(get_session)
):
    """Get all payments with optional filtering and pagination"""
    try:
        query = select(Payment)
        
        if resident_id:
            query = query.where(Payment.resident_id == resident_id)
        
        if unit_id:
            query = query.where(Payment.unit_id == unit_id)
        
        if payment_type:
            query = query.where(Payment.payment_type == payment_type)
        
        if status:
            query = query.where(Payment.status == status)
        
        if start_date:
            query = query.where(Payment.payment_date >= start_date)
        
        if end_date:
            query = query.where(Payment.payment_date <= end_date)
        
        query = query.offset(skip).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch payments: {str(e)}")

@router.get("/{payment_id}", response_model=PaymentOut)
async def get_payment(
    payment_id: int, 
    session: AsyncSession = Depends(get_session)
):
    """Get a specific payment by ID"""
    try:
        payment = await session.get(Payment, payment_id)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        return payment
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch payment: {str(e)}")

@router.put("/{payment_id}", response_model=PaymentOut)
async def update_payment(
    payment_id: int, 
    updates: PaymentUpdate, 
    session: AsyncSession = Depends(get_session)
):
    """Update a payment"""
    try:
        payment = await session.get(Payment, payment_id)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        
        update_data = updates.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(payment, key, value)
        
        await session.commit()
        await session.refresh(payment)
        return payment
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to update payment: {str(e)}")

@router.delete("/{payment_id}", status_code=204)
async def delete_payment(
    payment_id: int, 
    session: AsyncSession = Depends(get_session)
):
    """Delete a payment"""
    try:
        payment = await session.get(Payment, payment_id)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")

        await session.delete(payment)
        await session.commit()
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to delete payment: {str(e)}")

@router.get("/resident/{resident_id}", response_model=List[PaymentOut])
async def get_payments_by_resident(
    resident_id: int,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    session: AsyncSession = Depends(get_session)
):
    """Get all payments for a specific resident"""
    try:
        # Verify resident exists
        resident = await session.get(Resident, resident_id)
        if not resident:
            raise HTTPException(status_code=404, detail="Resident not found")
        
        query = select(Payment).where(Payment.resident_id == resident_id).offset(skip).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch payments: {str(e)}")

@router.get("/unit/{unit_id}", response_model=List[PaymentOut])
async def get_payments_by_unit(
    unit_id: int,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    session: AsyncSession = Depends(get_session)
):
    """Get all payments for a specific unit"""
    try:
        # Verify unit exists
        unit = await session.get(Unit, unit_id)
        if not unit:
            raise HTTPException(status_code=404, detail="Unit not found")
        
        query = select(Payment).where(Payment.unit_id == unit_id).offset(skip).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch payments: {str(e)}")

@router.get("/stats/summary", response_model=dict)
async def get_payment_summary(
    start_date: Optional[date] = Query(None, description="Start date for summary"),
    end_date: Optional[date] = Query(None, description="End date for summary"),
    session: AsyncSession = Depends(get_session)
):
    """Get payment summary statistics"""
    try:
        query = select(
            func.sum(Payment.amount).label("total_amount"),
            func.count(Payment.id).label("total_payments"),
            func.avg(Payment.amount).label("average_payment")
        )
        
        if start_date:
            query = query.where(Payment.payment_date >= start_date)
        
        if end_date:
            query = query.where(Payment.payment_date <= end_date)
        
        result = await session.execute(query)
        summary = result.first()
        
        return {
            "total_amount": float(summary.total_amount or 0),
            "total_payments": summary.total_payments or 0,
            "average_payment": float(summary.average_payment or 0),
            "date_range": {
                "start_date": start_date.isoformat() if start_date else None,
                "end_date": end_date.isoformat() if end_date else None
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch payment summary: {str(e)}") 