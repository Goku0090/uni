FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Copy everything
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r auth_project/requirements.txt

# Make start script executable
RUN chmod +x start.sh

# Expose port
EXPOSE 8000

# Run start script
CMD ["./start.sh"]
