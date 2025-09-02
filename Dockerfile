# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create reports directory
RUN mkdir -p reports logs

# Set environment variables
ENV PYTHONPATH=/app
ENV BASE_URL=https://reqres.in
ENV TIMEOUT=30
ENV RETRY_COUNT=3
ENV PARALLEL_WORKERS=4
ENV LOG_LEVEL=INFO

# Default command
CMD ["pytest", "-v", "--html=reports/report.html", "--self-contained-html", "--junit-xml=reports/junit.xml"]
