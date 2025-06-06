FROM python:3.10-slim

WORKDIR /app

# Copy and install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend Python files and folders
COPY backend/*.py .
COPY backend/database ./database
COPY backend/question ./question

# Copy frontend folder (with static and templates)
COPY frontend ./frontend

# Expose port for FastAPI
EXPOSE 8000

# Run FastAPI app using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
