from sqlalchemy import Column, Integer, String, ARRAY
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    role = Column(String, index=True)
    unit_number = Column(String, index=True)
    permissions = Column(ARRAY(String), default=[])