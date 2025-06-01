# Use an official, minimal Python image
FROM python:3.11-slim-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory in the container
WORKDIR /app

# Install build dependencies (for pip, some packages, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY . .

# Expose the port your app runs on (default Flask port)
EXPOSE 5000

# Set environment variable for Flask
ENV FLASK_APP=run.py

# Default command: run your app (you can change to gunicorn for production)
CMD ["python", "run.py"]
