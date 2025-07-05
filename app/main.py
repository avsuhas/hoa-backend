from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select 
from .database import get_session, engine, Base
from .models import User
from .schemas import UserOut
from typing import List
from .routes import users 
from .routes import emergency_contacts

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
def read_root():
	return {"message": "Backend APIs for HOA"}


app.include_router(users.router)
app.include_router(emergency_contacts.router)