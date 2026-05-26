# =====================================================================
# FILE: Dockerfile
# Purpose: Containerization Layer for FastAPI & Streamlit Stack
# =====================================================================

# Step 1: Use official lightweight Python base image
FROM python:3.12-slim

# Step 2: Set environmental strict footprints
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Step 3: Establish working environment scope
WORKDIR /app

# Step 4: Install essential OS binaries for networking and compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Step 5: Copy dependencies blueprint list first
COPY requirements.txt .

# Step 6: Install dependencies globally inside the container grid
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Step 7: Copy the rest of your core codebase structures
COPY . .

# Step 8: Expose networking ports (FastAPI: 8000)
EXPOSE 8000

# Step 9: Launch processes
CMD ["sh", "-c", "PYTHONPATH=.:./app uvicorn app.main:app --host 0.0.0.0 --port 8000"]