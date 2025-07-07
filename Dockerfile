# Dockerfile
# Render needs to have lower python version to deploy the python FastAPI app. 
# Render currently does not expose a "Python Version" setting in the dashboard for web services and 
# uses the latest version of Python 3.13 by default
# For Render platform constraints we need python 3.11 version, That needs to use lower version of SQLAlchemy.  
# This a hack to get the app to work on Render. 

FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy your code
COPY . .

# Run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
