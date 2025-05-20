# Use official Python image as base
FROM python:3.11.12-slim

# Set working directory inside container
WORKDIR /app

# Install system dependencies for mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose port
EXPOSE 8080

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]


# docker compose up --build
# docker compose up -d  ( Used when you only stop container)
# docker ps
# docker exec -it hotel_mysql mysql -u root -p (To check database)
# docker compose stop
# docker compose down