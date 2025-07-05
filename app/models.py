from sqlalchemy import Column, String, Boolean, DateTime, Enum, ARRAY, Integer, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from .database import Base
import enum

# Define Enum for role
class UserRole(enum.Enum):
    super_admin = "super_admin"
    admin = "admin"
    board = "board"
    resident = "resident"
    tenant = "tenant" 

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    role = Column(Enum(UserRole), nullable=False)
    permissions = Column(ARRAY(String), default=[])
    is_active = Column(Boolean, default=True)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())


class EmergencyContact(Base):
    __tablename__ = "emergency_contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    relationship = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=True)


class VehicleInfo(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    color = Column(String, nullable=False)
    license_plate = Column(String, unique=True, nullable=False)
    parking_spot = Column(String, nullable=True)


class PetType(enum.Enum):
    dog = "dog"
    cat = "cat"
    bird = "bird"
    fish = "fish"
    other = "other"

class PetInfo(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(Enum(PetType), nullable=False)
    breed = Column(String, nullable=True)
    weight = Column(Float, nullable=True)
    registration_number = Column(String, nullable=True)


class MaintenanceWorkLog(Base):
    __tablename__ = "maintenance_work_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    maintenance_request_id = Column(UUID(as_uuid=True), nullable=False)
    worker_id = Column(UUID(as_uuid=True), nullable=False)
    worker_name = Column(String, nullable=False)
    work_date = Column(DateTime(timezone=True), nullable=False)
    hours_worked = Column(Float, nullable=False)
    work_description = Column(String, nullable=False)
    materials_used = Column(ARRAY(String), nullable=True)
    cost = Column(Float, nullable=True)
    images = Column(ARRAY(String), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

