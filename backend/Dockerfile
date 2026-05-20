# Use official Python runtime as a parent image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy the entire backend and necessary logic
# Assuming build context is the `scratch` root directory
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# We need the data, src, backend, and llm folders
COPY data/ /app/data/
COPY backend/ /app/backend/
COPY llm/ /app/llm/
COPY .env /app/.env

# Expose port
EXPOSE 8000

# Run FastAPI server using uvicorn
CMD ["uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "8000"]
