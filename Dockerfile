# --- Stage 1: Build Stage ---
# We use a full version of Python to install and compile everything
FROM python:3.11-slim as builder

WORKDIR /app

# Install dependencies in a temporary location
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# --- Stage 2: Runtime Stage ---
# We use a very tiny version of Python for the final container
FROM python:3.11-slim
WORKDIR /app

# Copy only the installed libraries from the builder stage
COPY --from=builder /root/.local /root/.local
# Copy your actual code
COPY . .

# Ensure the app can find the installed libraries
ENV PATH=/root/.local/bin:$PATH

# Streamlit runs on port 8501 by default
EXPOSE 8501

# Command to start the app
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]