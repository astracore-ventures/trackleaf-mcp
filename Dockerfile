FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install minimal build deps in case some packages require compilation
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Run as non-root
RUN useradd -m app && chown -R app:app /app
USER app

ENTRYPOINT ["python", "trackleaf_mcp.py"]
