# FastAPI Backend with Neon PostgreSQL

This project is a FastAPI backend API connected to a Neon PostgreSQL database. 

---

## 🚀 Getting Started

### 1. Create a Virtual Environment  

python -m venv venv

source venv/bin/activate     # On Windows: venv\Scripts\activate

### 2. Install Dependencies

pip install -r requirements.txt


### 3. Create a .env File
DATABASE_URL=?
 

### 4.▶️ Run the API Server

uvicorn app.main:app --reload


The API will be available at: http://127.0.0.1:8000

Interactive API docs: http://127.0.0.1:8000/docs


### 5.💾 Save Dependencies

pip freeze > requirements.txt
