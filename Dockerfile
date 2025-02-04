# Dockerfile for API Documentation Extractor

# Use a Python base image
FROM python:3.13-slim

# Set the working directory
WORKDIR /app

# Copy necessary files
COPY requirements.txt .
COPY extract_api_info.py .
COPY temporal_activity.py .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Entry point: Run the CLI-based extractor script
ENTRYPOINT ["python", "extract_api_info.py"]
