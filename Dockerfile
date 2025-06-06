# Use official Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy backend code
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/*.py ./
COPY backend/database ./database
COPY backend/question ./question

# Copy frontend (static & templates)
COPY frontend/static ./frontend/static
COPY frontend/templates ./frontend/templates

# Expose port and start FastAPI
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
