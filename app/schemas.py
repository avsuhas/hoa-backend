#pydantic Schema

from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from uuid import UUID
from .models import UserRole
from .models import PetType
from .models import PropertyType


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


class MaintenanceWorkLogCreate(BaseModel):
    maintenance_request_id: UUID
    worker_id: UUID
    worker_name: str
    work_date: datetime
    hours_worked: float
    work_description: str
    materials_used: Optional[List[str]] = None
    cost: Optional[float] = None
    images: Optional[List[str]] = None

class MaintenanceWorkLogUpdate(BaseModel):
    worker_name: Optional[str]
    work_date: Optional[datetime]
    hours_worked: Optional[float]
    work_description: Optional[str]
    materials_used: Optional[List[str]]
    cost: Optional[float]
    images: Optional[List[str]]

class MaintenanceWorkLogOut(BaseModel):
    id: UUID
    maintenance_request_id: UUID
    worker_id: UUID
    worker_name: str
    work_date: datetime
    hours_worked: float
    work_description: str
    materials_used: Optional[List[str]]
    cost: Optional[float]
    images: Optional[List[str]]
    created_at: datetime

class PropertyCreate(BaseModel):
    name: str
    address: str
    city: str
    state: str
    zip_code: str
    property_type: PropertyType
    total_units: int
    year_built: int
    amenities: List[str]
    management_company: Optional[str] = None
    is_active: bool = True

class PropertyUpdate(BaseModel):
    name: Optional[str]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip_code: Optional[str]
    property_type: Optional[PropertyType]
    total_units: Optional[int]
    year_built: Optional[int]
    amenities: Optional[List[str]]
    management_company: Optional[str]
    is_active: Optional[bool]

class PropertyOut(BaseModel):
    id: UUID
    name: str
    address: str
    city: str
    state: str
    zip_code: str
    property_type: PropertyType
    total_units: int
    year_built: int
    amenities: List[str]
    management_company: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
