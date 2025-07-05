from sqlalchemy import Column, String, Boolean, DateTime, Enum, ARRAY, Integer
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