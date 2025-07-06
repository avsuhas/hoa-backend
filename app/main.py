from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select 
from .database import get_session, engine, Base
from typing import List

# Import all route modules
from .routes import properties
from .routes import units
from .routes import residents
from .routes import payments
from .routes import maintenance
from .routes import violations
from .routes import contractors
from .routes import maintenance_enhanced
from .routes import users
from .routes import residents_enhanced

app = FastAPI(
    title="HOA Management System API",
    description="A comprehensive API for managing Homeowners Association operations",
    version="1.0.0"
)

@app.on_event("startup")
async def startup():
    if os.getenv("VERCEL") != "1":
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

@app.get("/")
def read_root():
	return {
        "message": "HOA Management System API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# Include all routers
app.include_router(properties.router)
app.include_router(units.router)
app.include_router(residents.router)
app.include_router(payments.router)
app.include_router(maintenance.router)
app.include_router(violations.router)
app.include_router(contractors.router)
app.include_router(maintenance_enhanced.router)
app.include_router(users.router)
app.include_router(residents_enhanced.router)
