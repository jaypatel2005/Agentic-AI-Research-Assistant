# --- Stage 1: Build Stage ---
FROM python:3.11-slim as builder

WORKDIR /app

# 1. Install system build dependencies (Required for installing Python packages like Cairo)
RUN apt-get update && apt-get install -y \
    build-essential \
    libcairo2-dev \
    pkg-config \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. Install Python dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# --- Stage 2: Runtime Stage ---
FROM python:3.11-slim
WORKDIR /app

# 3. Install runtime system dependencies (Required for PDF generation to WORK)
# We need libcairo2 and libpango at runtime, not just build time.
RUN apt-get update && apt-get install -y \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy installed Python libraries from builder
COPY --from=builder /root/.local /root/.local

# 5. Copy your actual application code
COPY . .

# 6. Set environment variables
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

# 7. Expose the port
EXPOSE 8501

# 8. Start the app (Updated to app.py)
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]