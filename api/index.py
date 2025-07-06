# api/index.py

from fastapi import FastAPI
from mangum import Mangum
from app.main import app  # reuse your existing FastAPI app

handler = Mangum(app)
