# ============================================================
# Dockerfile for ABM Construction Safety Simulation
# ============================================================

FROM python:3.11-slim

# Python runtime tweaks
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# System dependencies (for matplotlib backend)
RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc \
        libfreetype6-dev \
        libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies (cached layer)
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Application code
COPY . .

# Ensure results directory exists
RUN mkdir -p results

# Default command: run simulation + plots
CMD ["python", "-m", "src.visualize"]