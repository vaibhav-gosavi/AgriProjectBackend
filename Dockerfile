# Step 1: Use an official Python runtime as a base image
FROM python:3.12-slim

# Step 2: Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Step 3: Set working directory
WORKDIR /app

# Step 4: Install dependencies
COPY requirements_prod.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements_prod.txt

# Step 5: Copy the application code
COPY . .

# Step 6: Expose port
EXPOSE 8000

# Step 7: Run the FastAPI application
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
