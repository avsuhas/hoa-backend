# routes/emergency_contacts.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from ..database import get_session
from ..models import EmergencyContact
from ..schemas import EmergencyContactCreate, EmergencyContactUpdate, EmergencyContactOut

router = APIRouter(prefix="/emergency-contacts", tags=["Emergency Contacts"])

@router.post("/", response_model=EmergencyContactOut)
async def create_contact(contact: EmergencyContactCreate, session: AsyncSession = Depends(get_session)):
    new_contact = EmergencyContact(**contact.dict())
    session.add(new_contact)
    await session.commit()
    await session.refresh(new_contact)
    return new_contact

@router.get("/", response_model=List[EmergencyContactOut])
async def list_contacts(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(EmergencyContact))
    return result.scalars().all()

@router.get("/{contact_id}", response_model=EmergencyContactOut)
async def get_contact(contact_id: int, session: AsyncSession = Depends(get_session)):
    contact = await session.get(EmergencyContact, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.put("/{contact_id}", response_model=EmergencyContactOut)
async def update_contact(contact_id: int, updates: EmergencyContactUpdate, session: AsyncSession = Depends(get_session)):
    contact = await session.get(EmergencyContact, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(contact, key, value)

    await session.commit()
    await session.refresh(contact)
    return contact

@router.delete("/{contact_id}", status_code=204)
async def delete_contact(contact_id: int, session: AsyncSession = Depends(get_session)):
    contact = await session.get(EmergencyContact, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    await session.delete(contact)
    await session.commit()
