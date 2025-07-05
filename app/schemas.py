#pydantic Schema

from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from .models import UserRole
from .models import PetType
from uuid import UUID

class Config:
    orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    phone: Optional[str] = None
    role: UserRole
    permissions: List[str] = []


class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    role: Optional[UserRole]
    permissions: Optional[List[str]]
    is_active: Optional[bool]
    last_login_at: Optional[datetime]

class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    first_name: str
    last_name: str
    phone: Optional[str] = None
    role: UserRole
    permissions: List[str]
    is_active: bool
    last_login_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class EmergencyContactCreate(BaseModel):
    name: str
    relationship: str
    phone: str
    email: Optional[EmailStr] = None

class EmergencyContactUpdate(BaseModel):
    name: Optional[str]
    relationship: Optional[str]
    phone: Optional[str]
    email: Optional[EmailStr] = None

class EmergencyContactOut(BaseModel):
    id: int
    name: str
    relationship: str
    phone: str
    email: Optional[str]


class VehicleInfoCreate(BaseModel):
    make: str
    model: str
    year: int
    color: str
    license_plate: str
    parking_spot: Optional[str] = None

class VehicleInfoUpdate(BaseModel):
    make: Optional[str]
    model: Optional[str]
    year: Optional[int]
    color: Optional[str]
    license_plate: Optional[str]
    parking_spot: Optional[str]

class VehicleInfoOut(BaseModel):
    id: int
    make: str
    model: str
    year: int
    color: str
    license_plate: str
    parking_spot: Optional[str]

class PetInfoCreate(BaseModel):
    name: str
    type: PetType
    breed: Optional[str] = None
    weight: Optional[float] = None
    registration_number: Optional[str] = None

class PetInfoUpdate(BaseModel):
    name: Optional[str]
    type: Optional[PetType]
    breed: Optional[str]
    weight: Optional[float]
    registration_number: Optional[str]

class PetInfoOut(BaseModel):
    id: int
    name: str
    type: PetType
    breed: Optional[str]
    weight: Optional[float]
    registration_number: Optional[str]

    
