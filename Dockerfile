FROM python:3.11-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Copy and install requirements
COPY auth_project/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Make scripts executable  
RUN chmod +x start.sh

EXPOSE 8000

# Run migrations and start server
CMD ["bash", "start.sh"]
