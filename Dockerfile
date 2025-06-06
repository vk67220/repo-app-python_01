FROM python:3.10

WORKDIR /app

# Copy backend code
COPY backend/ .

# Copy frontend (static and templates) into container
COPY frontend/ frontend/

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
