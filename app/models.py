from sqlalchemy import Column, String, Boolean, DateTime, Enum, Integer, Float, Date, Time, Text, Numeric, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from .database import Base
import enum

# Enums
class ResidentType(enum.Enum):
    owner = "Owner"
    tenant = "Tenant"
    board_member = "Board Member"

class AccountType(enum.Enum):
    operating = "Operating"
    reserve = "Reserve"
    special_assessment = "Special Assessment"

class PaymentType(enum.Enum):
    monthly_fee = "Monthly Fee"
    special_assessment = "Special Assessment"
    late_fee = "Late Fee"
    other = "Other"

class PaymentStatus(enum.Enum):
    paid = "Paid"
    pending = "Pending"
    overdue = "Overdue"
    partial = "Partial"

class Priority(enum.Enum):
    low = "Low"
    medium = "Medium"
    high = "High"
    emergency = "Emergency"

class MaintenanceStatus(enum.Enum):
    pending = "Pending"
    in_progress = "In Progress"
    scheduled = "Scheduled"
    completed = "Completed"
    cancelled = "Cancelled"

class ViolationSeverity(enum.Enum):
    minor = "Minor"
    major = "Major"
    severe = "Severe"

class ViolationStatus(enum.Enum):
    open = "Open"
    warning_sent = "Warning Sent"
    fine_issued = "Fine Issued"
    resolved = "Resolved"
    escalated = "Escalated"

class MeetingType(enum.Enum):
    board_meeting = "Board Meeting"
    annual_meeting = "Annual Meeting"
    special_meeting = "Special Meeting"
    committee_meeting = "Committee Meeting"

class MeetingStatus(enum.Enum):
    scheduled = "Scheduled"
    in_progress = "In Progress"
    completed = "Completed"
    cancelled = "Cancelled"

class AccessLevel(enum.Enum):
    public = "Public"
    residents_only = "Residents Only"
    board_only = "Board Only"
    admin_only = "Admin Only"

class BillingFrequency(enum.Enum):
    monthly = "Monthly"
    quarterly = "Quarterly"
    annually = "Annually"
    one_time = "One-time"

# Models
class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    address = Column(Text, nullable=False)
    total_units = Column(Integer, nullable=False)
    property_type = Column(String(100), nullable=True)
    year_built = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relationships
    units = relationship("Unit", back_populates="property", cascade="all, delete-orphan")


class Unit(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    unit_number = Column(String(50), nullable=False)
    unit_type = Column(String(100), nullable=True)
    square_feet = Column(Integer, nullable=True)
    bedrooms = Column(Integer, nullable=True)
    bathrooms = Column(Numeric(2, 1), nullable=True)
    monthly_fee = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relationships
    property = relationship("Property", back_populates="units")
    residents = relationship("Resident", back_populates="unit", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="unit", cascade="all, delete-orphan")
    maintenance_requests = relationship("MaintenanceRequest", back_populates="unit", cascade="all, delete-orphan")
    violations = relationship("Violation", back_populates="unit", cascade="all, delete-orphan")


class Resident(Base):
    __tablename__ = "residents"

    id = Column(Integer, primary_key=True, index=True)
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    resident_type = Column(Enum(ResidentType), nullable=False)
    move_in_date = Column(Date, nullable=True)
    emergency_contact_name = Column(String(200), nullable=True)
    emergency_contact_phone = Column(String(20), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relationships
    unit = relationship("Unit", back_populates="residents")
    payments = relationship("Payment", back_populates="resident", cascade="all, delete-orphan")
    maintenance_requests = relationship("MaintenanceRequest", back_populates="resident", cascade="all, delete-orphan")
    violations = relationship("Violation", back_populates="resident", cascade="all, delete-orphan")


class FinancialAccount(Base):
    __tablename__ = "financial_accounts"

    id = Column(Integer, primary_key=True, index=True)
    account_name = Column(String(255), nullable=False)
    account_type = Column(Enum(AccountType), nullable=False)
    balance = Column(Numeric(12, 2), default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    resident_id = Column(Integer, ForeignKey("residents.id"), nullable=False)
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    payment_type = Column(Enum(PaymentType), nullable=False)
    payment_method = Column(String(50), nullable=True)
    payment_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=True)
    status = Column(Enum(PaymentStatus), nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    resident = relationship("Resident", back_populates="payments")
    unit = relationship("Unit", back_populates="payments")


class MaintenanceRequest(Base):
    __tablename__ = "maintenance_requests"

    id = Column(Integer, primary_key=True, index=True)
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=False)
    resident_id = Column(Integer, ForeignKey("residents.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(Enum(Priority), nullable=False)
    status = Column(Enum(MaintenanceStatus), nullable=False)
    category = Column(String(100), nullable=True)
    estimated_cost = Column(Numeric(10, 2), nullable=True)
    actual_cost = Column(Numeric(10, 2), nullable=True)
    assigned_to = Column(String(255), nullable=True)
    scheduled_date = Column(Date, nullable=True)
    completed_date = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relationships
    unit = relationship("Unit", back_populates="maintenance_requests")
    resident = relationship("Resident", back_populates="maintenance_requests")


class Violation(Base):
    __tablename__ = "violations"

    id = Column(Integer, primary_key=True, index=True)
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=False)
    resident_id = Column(Integer, ForeignKey("residents.id"), nullable=False)
    violation_type = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(Enum(ViolationSeverity), nullable=False)
    status = Column(Enum(ViolationStatus), nullable=False)
    fine_amount = Column(Numeric(10, 2), nullable=True)
    inspection_date = Column(Date, nullable=True)
    resolution_date = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relationships
    unit = relationship("Unit", back_populates="violations")
    resident = relationship("Resident", back_populates="violations")


class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    meeting_type = Column(Enum(MeetingType), nullable=False)
    meeting_date = Column(Date, nullable=False)
    meeting_time = Column(Time, nullable=False)
    location = Column(String(255), nullable=True)
    agenda = Column(Text, nullable=True)
    minutes = Column(Text, nullable=True)
    attendee_count = Column(Integer, default=0)
    status = Column(Enum(MeetingStatus), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    document_type = Column(String(100), nullable=True)
    file_path = Column(String(500), nullable=True)
    file_size = Column(Integer, nullable=True)
    uploaded_by = Column(String(255), nullable=True)
    access_level = Column(Enum(AccessLevel), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())


class ServiceProvider(Base):
    __tablename__ = "service_providers"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(255), nullable=False)
    contact_person = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    service_type = Column(String(100), nullable=True)
    hourly_rate = Column(Numeric(8, 2), nullable=True)
    is_preferred = Column(Boolean, default=False)
    insurance_expiry = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())


class ManagementFee(Base):
    __tablename__ = "management_fees"

    id = Column(Integer, primary_key=True, index=True)
    fee_type = Column(String(100), nullable=False)
    amount = Column(Numeric(10, 2), nullable=True)
    rate_per_unit = Column(Numeric(8, 2), nullable=True)
    billing_frequency = Column(Enum(BillingFrequency), nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

