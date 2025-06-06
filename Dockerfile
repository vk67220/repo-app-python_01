# backend/Dockerfile

FROM python:3.10-slim

WORKDIR /app

# Copy requirements.txt from backend folder in root context
COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy python source files from backend folder
COPY backend/*.py .

# Copy subfolders from backend folder
COPY backend/question ./question
COPY backend/database ./database

# Copy frontend folder (contains static and templates)
COPY frontend ./frontend

# Expose FastAPI default port
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
