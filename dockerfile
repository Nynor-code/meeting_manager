# Dockerfile
FROM --platform=linux/arm64 python:3.11-slim
#FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y \
    libcairo2 \
    libpango-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libjpeg-dev \
    libffi-dev \
    libpangoft2-1.0-0 \
    && rm -rf /var/lib/apt/lists/*
# libgobject-2.0-0 \


# Copy app files
COPY . .

# Expose port
EXPOSE 5000

# Run the app
# CMD ["flask", "run", "--host=0.0.0.0:5000"]
# Run the Flask application
CMD ["python", "app.py"]
