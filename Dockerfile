# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies and clean up
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Use a .dockerignore file to exclude unnecessary files and directories
# .dockerignore
# venv/
# __pycache__/
# *.pyc
# .git/
# .env
# *.log
# tests/

# Specify the entry point for the application
ENTRYPOINT ["python", "run.py"]
