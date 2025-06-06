# Use official Python image
FROM python:3.10

# Set working directory inside the container
WORKDIR /app

# Copy backend code
COPY backend/ .

# Copy frontend assets
COPY frontend/static frontend/static
COPY frontend/templates frontend/templates

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
