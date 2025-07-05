#pydantic Schema

from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from .models import UserRole
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