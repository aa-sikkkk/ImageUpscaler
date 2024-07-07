# Stage 1: Build stage
FROM python:3.11-slim AS builder

# Set the working directory
WORKDIR /app

# Copy only requirements.txt to the container
COPY requirements.txt .

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential gcc && \
    python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt && \
    apt-get purge -y --auto-remove build-essential gcc && \
    rm -rf /var/lib/apt/lists/*

# Stage 2: Final stage
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy only the necessary files from the build stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy the rest of the application code
COPY . .

# Specify the entry point for the application
ENTRYPOINT ["python", "run.py"]
