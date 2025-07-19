#pydantic Schema

from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime, date, time
from uuid import UUID
from decimal import Decimal
from .models import (
    ResidentType, AccountType, PaymentType, PaymentStatus, Priority, 
    MaintenanceStatus, ViolationSeverity, ViolationStatus, MeetingType, 
    MeetingStatus, AccessLevel, BillingFrequency, MaintenanceCategory,
    MaintenanceStatusEnhanced, PreferredTimeSlot, UserRole, ResidentTypeEnhanced
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

# Contractor Schemas
class ContractorCreate(BaseModel):
    name: str = Field(..., max_length=100)
    company: Optional[str] = Field(None, max_length=100)
    email: EmailStr
    phone: str = Field(..., max_length=20)
    specialties: Optional[List[str]] = Field(default=[])
    rating: Optional[Decimal] = Field(0.00, ge=0, le=5)
    is_active: Optional[bool] = True
    license_number: Optional[str] = Field(None, max_length=50)
    insurance_expiry: Optional[date]

    class Config:
        from_attributes = True

class ContractorUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    company: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr]
    phone: Optional[str] = Field(None, max_length=20)
    specialties: Optional[List[str]]
    rating: Optional[Decimal] = Field(None, ge=0, le=5)
    is_active: Optional[bool]
    license_number: Optional[str] = Field(None, max_length=50)
    insurance_expiry: Optional[date]

    class Config:
        from_attributes = True

class ContractorOut(BaseModel):
    id: UUID
    name: str
    company: Optional[str]
    email: str
    phone: str
    specialties: List[str]
    rating: Decimal
    is_active: bool
    license_number: Optional[str]
    insurance_expiry: Optional[date]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Enhanced Maintenance Request Schemas
class MaintenanceRequestEnhancedCreate(BaseModel):
    title: str = Field(..., max_length=200)
    description: str
    category: MaintenanceCategory
    priority: Priority
    status: Optional[MaintenanceStatusEnhanced] = MaintenanceStatusEnhanced.pending
    unit_id: UUID
    property_id: UUID
    resident_id: UUID
    assigned_to: Optional[str] = Field(None, max_length=100)
    assigned_to_name: Optional[str] = Field(None, max_length=100)
    contractor_id: Optional[UUID]
    estimated_cost: Optional[Decimal] = Field(None, ge=0)
    actual_cost: Optional[Decimal] = Field(None, ge=0)
    scheduled_date: Optional[datetime]
    completed_date: Optional[datetime]
    images: Optional[List[str]] = Field(default=[])
    notes: Optional[str]
    work_order_number: Optional[str] = Field(None, max_length=50)
    is_emergency: Optional[bool] = False
    access_instructions: Optional[str]
    preferred_time_slot: Optional[PreferredTimeSlot]
    resident_available: Optional[bool] = True
    created_by: UUID

    class Config:
        from_attributes = True

class MaintenanceRequestEnhancedUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str]
    category: Optional[MaintenanceCategory]
    priority: Optional[Priority]
    status: Optional[MaintenanceStatusEnhanced]
    assigned_to: Optional[str] = Field(None, max_length=100)
    assigned_to_name: Optional[str] = Field(None, max_length=100)
    contractor_id: Optional[UUID]
    estimated_cost: Optional[Decimal] = Field(None, ge=0)
    actual_cost: Optional[Decimal] = Field(None, ge=0)
    scheduled_date: Optional[datetime]
    completed_date: Optional[datetime]
    images: Optional[List[str]]
    notes: Optional[str]
    work_order_number: Optional[str] = Field(None, max_length=50)
    is_emergency: Optional[bool]
    access_instructions: Optional[str]
    preferred_time_slot: Optional[PreferredTimeSlot]
    resident_available: Optional[bool]
    updated_by: Optional[UUID]

    class Config:
        from_attributes = True

class MaintenanceRequestEnhancedOut(BaseModel):
    id: UUID
    title: str
    description: str
    category: MaintenanceCategory
    priority: Priority
    status: MaintenanceStatusEnhanced
    unit_id: UUID
    property_id: UUID
    resident_id: UUID
    assigned_to: Optional[str]
    assigned_to_name: Optional[str]
    contractor_id: Optional[UUID]
    estimated_cost: Optional[Decimal]
    actual_cost: Optional[Decimal]
    scheduled_date: Optional[datetime]
    completed_date: Optional[datetime]
    images: List[str]
    notes: Optional[str]
    work_order_number: Optional[str]
    is_emergency: bool
    access_instructions: Optional[str]
    preferred_time_slot: Optional[PreferredTimeSlot]
    resident_available: bool
    created_by: UUID
    updated_by: Optional[UUID]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Maintenance Work Log Schemas
class MaintenanceWorkLogCreate(BaseModel):
    maintenance_request_id: UUID
    worker_id: Optional[UUID]
    worker_name: str = Field(..., max_length=100)
    work_date: date
    hours_worked: Decimal = Field(..., ge=0)
    work_description: str
    materials_used: Optional[List[str]] = Field(default=[])
    cost: Optional[Decimal] = Field(0.00, ge=0)
    images: Optional[List[str]] = Field(default=[])
    created_by: UUID

    class Config:
        from_attributes = True

class MaintenanceWorkLogUpdate(BaseModel):
    worker_id: Optional[UUID]
    worker_name: Optional[str] = Field(None, max_length=100)
    work_date: Optional[date]
    hours_worked: Optional[Decimal] = Field(None, ge=0)
    work_description: Optional[str]
    materials_used: Optional[List[str]]
    cost: Optional[Decimal] = Field(None, ge=0)
    images: Optional[List[str]]

    class Config:
        from_attributes = True

class MaintenanceWorkLogOut(BaseModel):
    id: UUID
    maintenance_request_id: UUID
    worker_id: Optional[UUID]
    worker_name: str
    work_date: date
    hours_worked: Decimal
    work_description: str
    materials_used: List[str]
    cost: Decimal
    images: List[str]
    created_by: UUID
    created_at: datetime

    class Config:
        from_attributes = True

# Authentication Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRegister(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    # No role field

class UserApproval(BaseModel):
    user_id: str
    role: str  # Must be one of 'board_member', 'community_admin', 'property_manager'

class PasswordSetupRequest(BaseModel):
    token: str
    password: str

# User Schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    phone: Optional[str] = Field(None, max_length=20)
    role: Optional[UserRole] = UserRole.resident
    is_active: Optional[bool] = True
    email_verified: Optional[bool] = False

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    password_hash: Optional[str] = Field(None, max_length=255)
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    phone: Optional[str] = Field(None, max_length=20)
    role: Optional[UserRole]
    is_active: Optional[bool]
    email_verified: Optional[bool]

    class Config:
        from_attributes = True

class UserOut(BaseModel):
    id: UUID
    email: str
    first_name: str
    last_name: str
    phone: Optional[str]
    role: UserRole
    is_active: bool
    email_verified: bool
    last_login_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Enhanced Resident Schemas
class ResidentEnhancedCreate(BaseModel):
    user_id: Optional[UUID]
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    email: str = Field(..., max_length=255)
    phone: str = Field(..., max_length=20)
    unit_id: UUID
    property_id: UUID
    resident_type: ResidentTypeEnhanced
    role: Optional[UserRole] = UserRole.resident
    move_in_date: date
    move_out_date: Optional[date] = None
    lease_end_date: Optional[date] = None
    emergency_contact: dict
    vehicle_info: Optional[List[dict]] = Field(default=[])
    pet_info: Optional[List[dict]] = Field(default=[])
    is_active: Optional[bool] = True
    is_primary: Optional[bool] = False
    notes: Optional[str] = None
    created_by: UUID

    class Config:
        from_attributes = True

class ResidentEnhancedUpdate(BaseModel):
    user_id: Optional[UUID]
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    email: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    resident_type: Optional[ResidentTypeEnhanced]
    role: Optional[UserRole]
    move_out_date: Optional[date]
    lease_end_date: Optional[date]
    emergency_contact: Optional[dict]
    vehicle_info: Optional[List[dict]]
    pet_info: Optional[List[dict]]
    is_active: Optional[bool]
    is_primary: Optional[bool]
    notes: Optional[str]
    updated_by: Optional[UUID]

    class Config:
        from_attributes = True

class ResidentEnhancedOut(BaseModel):
    id: UUID
    user_id: Optional[UUID]
    first_name: str
    last_name: str
    email: str
    phone: str
    unit_id: UUID
    property_id: UUID
    resident_type: ResidentTypeEnhanced
    role: UserRole
    move_in_date: date
    move_out_date: Optional[date]
    lease_end_date: Optional[date]
    emergency_contact: dict
    vehicle_info: List[dict]
    pet_info: List[dict]
    is_active: bool
    is_primary: bool
    notes: Optional[str]
    created_by: UUID
    updated_by: Optional[UUID]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
