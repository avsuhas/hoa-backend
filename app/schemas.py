#pydantic Schema

from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime, date, time
from uuid import UUID
from decimal import Decimal
from .models import (
    ResidentType, AccountType, PaymentType, PaymentStatus, Priority, 
    MaintenanceStatus, ViolationSeverity, ViolationStatus, MeetingType, 
    MeetingStatus, AccessLevel, BillingFrequency
)

# Base Config
class Config:
    from_attributes = True

# Property Schemas
class PropertyCreate(BaseModel):
    name: str = Field(..., max_length=255)
    address: str
    total_units: int = Field(..., gt=0)
    property_type: Optional[str] = Field(None, max_length=100)
    year_built: Optional[int] = Field(None, gt=1800)

    class Config:
        from_attributes = True

class PropertyUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    address: Optional[str]
    total_units: Optional[int] = Field(None, gt=0)
    property_type: Optional[str] = Field(None, max_length=100)
    year_built: Optional[int] = Field(None, gt=1800)

    class Config:
        from_attributes = True

class PropertyOut(BaseModel):
    id: int
    name: str
    address: str
    total_units: int
    property_type: Optional[str]
    year_built: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Unit Schemas
class UnitCreate(BaseModel):
    property_id: int
    unit_number: str = Field(..., max_length=50)
    unit_type: Optional[str] = Field(None, max_length=100)
    square_feet: Optional[int] = Field(None, gt=0)
    bedrooms: Optional[int] = Field(None, ge=0)
    bathrooms: Optional[Decimal] = Field(None, ge=0)
    monthly_fee: Decimal = Field(..., ge=0)

    class Config:
        from_attributes = True

class UnitUpdate(BaseModel):
    unit_number: Optional[str] = Field(None, max_length=50)
    unit_type: Optional[str] = Field(None, max_length=100)
    square_feet: Optional[int] = Field(None, gt=0)
    bedrooms: Optional[int] = Field(None, ge=0)
    bathrooms: Optional[Decimal] = Field(None, ge=0)
    monthly_fee: Optional[Decimal] = Field(None, ge=0)

    class Config:
        from_attributes = True

class UnitOut(BaseModel):
    id: int
    property_id: int
    unit_number: str
    unit_type: Optional[str]
    square_feet: Optional[int]
    bedrooms: Optional[int]
    bathrooms: Optional[Decimal]
    monthly_fee: Decimal
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Resident Schemas
class ResidentCreate(BaseModel):
    unit_id: int
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    resident_type: ResidentType
    move_in_date: Optional[date]
    emergency_contact_name: Optional[str] = Field(None, max_length=200)
    emergency_contact_phone: Optional[str] = Field(None, max_length=20)

    class Config:
        from_attributes = True

class ResidentUpdate(BaseModel):
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr]
    phone: Optional[str] = Field(None, max_length=20)
    resident_type: Optional[ResidentType]
    move_in_date: Optional[date]
    emergency_contact_name: Optional[str] = Field(None, max_length=200)
    emergency_contact_phone: Optional[str] = Field(None, max_length=20)

    class Config:
        from_attributes = True

class ResidentOut(BaseModel):
    id: int
    unit_id: int
    first_name: str
    last_name: str
    email: str
    phone: Optional[str]
    resident_type: ResidentType
    move_in_date: Optional[date]
    emergency_contact_name: Optional[str]
    emergency_contact_phone: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Financial Account Schemas
class FinancialAccountCreate(BaseModel):
    account_name: str = Field(..., max_length=255)
    account_type: AccountType
    balance: Optional[Decimal] = Field(0, ge=0)

    class Config:
        from_attributes = True

class FinancialAccountUpdate(BaseModel):
    account_name: Optional[str] = Field(None, max_length=255)
    account_type: Optional[AccountType]
    balance: Optional[Decimal] = Field(None, ge=0)

    class Config:
        from_attributes = True

class FinancialAccountOut(BaseModel):
    id: int
    account_name: str
    account_type: AccountType
    balance: Decimal
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Payment Schemas
class PaymentCreate(BaseModel):
    resident_id: int
    unit_id: int
    amount: Decimal = Field(..., gt=0)
    payment_type: PaymentType
    payment_method: Optional[str] = Field(None, max_length=50)
    payment_date: date
    due_date: Optional[date]
    status: PaymentStatus
    notes: Optional[str]

    class Config:
        from_attributes = True

class PaymentUpdate(BaseModel):
    amount: Optional[Decimal] = Field(None, gt=0)
    payment_type: Optional[PaymentType]
    payment_method: Optional[str] = Field(None, max_length=50)
    payment_date: Optional[date]
    due_date: Optional[date]
    status: Optional[PaymentStatus]
    notes: Optional[str]

    class Config:
        from_attributes = True

class PaymentOut(BaseModel):
    id: int
    resident_id: int
    unit_id: int
    amount: Decimal
    payment_type: PaymentType
    payment_method: Optional[str]
    payment_date: date
    due_date: Optional[date]
    status: PaymentStatus
    notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

# Maintenance Request Schemas
class MaintenanceRequestCreate(BaseModel):
    unit_id: int
    resident_id: int
    title: str = Field(..., max_length=255)
    description: Optional[str]
    priority: Priority
    status: MaintenanceStatus
    category: Optional[str] = Field(None, max_length=100)
    estimated_cost: Optional[Decimal] = Field(None, ge=0)
    actual_cost: Optional[Decimal] = Field(None, ge=0)
    assigned_to: Optional[str] = Field(None, max_length=255)
    scheduled_date: Optional[date]
    completed_date: Optional[date]

    class Config:
        from_attributes = True

class MaintenanceRequestUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str]
    priority: Optional[Priority]
    status: Optional[MaintenanceStatus]
    category: Optional[str] = Field(None, max_length=100)
    estimated_cost: Optional[Decimal] = Field(None, ge=0)
    actual_cost: Optional[Decimal] = Field(None, ge=0)
    assigned_to: Optional[str] = Field(None, max_length=255)
    scheduled_date: Optional[date]
    completed_date: Optional[date]

    class Config:
        from_attributes = True

class MaintenanceRequestOut(BaseModel):
    id: int
    unit_id: int
    resident_id: int
    title: str
    description: Optional[str]
    priority: Priority
    status: MaintenanceStatus
    category: Optional[str]
    estimated_cost: Optional[Decimal]
    actual_cost: Optional[Decimal]
    assigned_to: Optional[str]
    scheduled_date: Optional[date]
    completed_date: Optional[date]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Violation Schemas
class ViolationCreate(BaseModel):
    unit_id: int
    resident_id: int
    violation_type: str = Field(..., max_length=255)
    description: str
    severity: ViolationSeverity
    status: ViolationStatus
    fine_amount: Optional[Decimal] = Field(None, ge=0)
    inspection_date: Optional[date]
    resolution_date: Optional[date]
    notes: Optional[str]

    class Config:
        from_attributes = True

class ViolationUpdate(BaseModel):
    violation_type: Optional[str] = Field(None, max_length=255)
    description: Optional[str]
    severity: Optional[ViolationSeverity]
    status: Optional[ViolationStatus]
    fine_amount: Optional[Decimal] = Field(None, ge=0)
    inspection_date: Optional[date]
    resolution_date: Optional[date]
    notes: Optional[str]

    class Config:
        from_attributes = True

class ViolationOut(BaseModel):
    id: int
    unit_id: int
    resident_id: int
    violation_type: str
    description: str
    severity: ViolationSeverity
    status: ViolationStatus
    fine_amount: Optional[Decimal]
    inspection_date: Optional[date]
    resolution_date: Optional[date]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Meeting Schemas
class MeetingCreate(BaseModel):
    title: str = Field(..., max_length=255)
    meeting_type: MeetingType
    meeting_date: date
    meeting_time: time
    location: Optional[str] = Field(None, max_length=255)
    agenda: Optional[str]
    minutes: Optional[str]
    attendee_count: Optional[int] = Field(0, ge=0)
    status: MeetingStatus

    class Config:
        from_attributes = True

class MeetingUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    meeting_type: Optional[MeetingType]
    meeting_date: Optional[date]
    meeting_time: Optional[time]
    location: Optional[str] = Field(None, max_length=255)
    agenda: Optional[str]
    minutes: Optional[str]
    attendee_count: Optional[int] = Field(None, ge=0)
    status: Optional[MeetingStatus]

    class Config:
        from_attributes = True

class MeetingOut(BaseModel):
    id: int
    title: str
    meeting_type: MeetingType
    meeting_date: date
    meeting_time: time
    location: Optional[str]
    agenda: Optional[str]
    minutes: Optional[str]
    attendee_count: int
    status: MeetingStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Document Schemas
class DocumentCreate(BaseModel):
    title: str = Field(..., max_length=255)
    document_type: Optional[str] = Field(None, max_length=100)
    file_path: Optional[str] = Field(None, max_length=500)
    file_size: Optional[int] = Field(None, ge=0)
    uploaded_by: Optional[str] = Field(None, max_length=255)
    access_level: AccessLevel

    class Config:
        from_attributes = True

class DocumentUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    document_type: Optional[str] = Field(None, max_length=100)
    file_path: Optional[str] = Field(None, max_length=500)
    file_size: Optional[int] = Field(None, ge=0)
    uploaded_by: Optional[str] = Field(None, max_length=255)
    access_level: Optional[AccessLevel]

    class Config:
        from_attributes = True

class DocumentOut(BaseModel):
    id: int
    title: str
    document_type: Optional[str]
    file_path: Optional[str]
    file_size: Optional[int]
    uploaded_by: Optional[str]
    access_level: AccessLevel
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Service Provider Schemas
class ServiceProviderCreate(BaseModel):
    company_name: str = Field(..., max_length=255)
    contact_person: Optional[str] = Field(None, max_length=255)
    email: Optional[EmailStr]
    phone: Optional[str] = Field(None, max_length=20)
    service_type: Optional[str] = Field(None, max_length=100)
    hourly_rate: Optional[Decimal] = Field(None, ge=0)
    is_preferred: Optional[bool] = False
    insurance_expiry: Optional[date]

    class Config:
        from_attributes = True

class ServiceProviderUpdate(BaseModel):
    company_name: Optional[str] = Field(None, max_length=255)
    contact_person: Optional[str] = Field(None, max_length=255)
    email: Optional[EmailStr]
    phone: Optional[str] = Field(None, max_length=20)
    service_type: Optional[str] = Field(None, max_length=100)
    hourly_rate: Optional[Decimal] = Field(None, ge=0)
    is_preferred: Optional[bool]
    insurance_expiry: Optional[date]

    class Config:
        from_attributes = True

class ServiceProviderOut(BaseModel):
    id: int
    company_name: str
    contact_person: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    service_type: Optional[str]
    hourly_rate: Optional[Decimal]
    is_preferred: bool
    insurance_expiry: Optional[date]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Management Fee Schemas
class ManagementFeeCreate(BaseModel):
    fee_type: str = Field(..., max_length=100)
    amount: Optional[Decimal] = Field(None, ge=0)
    rate_per_unit: Optional[Decimal] = Field(None, ge=0)
    billing_frequency: BillingFrequency
    description: Optional[str]
    is_active: Optional[bool] = True

    class Config:
        from_attributes = True

class ManagementFeeUpdate(BaseModel):
    fee_type: Optional[str] = Field(None, max_length=100)
    amount: Optional[Decimal] = Field(None, ge=0)
    rate_per_unit: Optional[Decimal] = Field(None, ge=0)
    billing_frequency: Optional[BillingFrequency]
    description: Optional[str]
    is_active: Optional[bool]

    class Config:
        from_attributes = True

class ManagementFeeOut(BaseModel):
    id: int
    fee_type: str
    amount: Optional[Decimal]
    rate_per_unit: Optional[Decimal]
    billing_frequency: BillingFrequency
    description: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
