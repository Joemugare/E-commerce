# ------------------------------------------------------------------------------  
# Production-ready Django Dockerfile for Render or Docker Compose  
# ------------------------------------------------------------------------------

FROM python:3.12-slim

# --- Environment Variables ---
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# --- System Dependencies ---
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    curl \
    libjpeg-dev \
    zlib1g-dev \
    python3-tk \
    tk-dev \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# --- Set Working Directory ---
WORKDIR /app

# --- Install Python Dependencies ---
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir -r requirements.txt

# --- Copy Project Code ---
COPY . .

# --- Collect Static Files ---
RUN python manage.py collectstatic --noinput

# --- Expose Port & Run Server ---
EXPOSE 8000
CMD ["gunicorn", "store_project.wsgi:application", "--bind", "0.0.0.0:8000"]
