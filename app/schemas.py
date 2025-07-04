#schemas.py

# schemas.py

from pydantic import BaseModel, EmailStr
from typing import List

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    unit_number: str
    permissions: List[str] = []
    
    class Config:
        orm_mode = True  # ✅ Needed for SQLAlchemy ORM integration
