# api/index.py

from mangum import Mangum
from app.main import app  # reuse your existing FastAPI app

print("✔ Booting Mangum handler for FastAPI on Vercel")  # ✅ debug
handler = Mangum(app)
