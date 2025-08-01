FROM python:3.12-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    curl \
    libjpeg-dev \
    zlib1g-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Configure pip
RUN pip config set global.index-url https://pypi.org/simple
RUN python -m pip install --default-timeout=100 --upgrade pip setuptools wheel

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt

# Copy project files
COPY . .

# Collect static files for whitenoise
RUN python manage.py collectstatic --noinput

# Run development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
