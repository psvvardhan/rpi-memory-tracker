FROM python:3.9-slim

WORKDIR /app

# Install required packages
RUN apt-get update && apt-get install -y \
    coreutils \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Copy application code
COPY app.py /app/
COPY templates/index.html /app/templates/

# Install Python dependencies
RUN pip install --no-cache-dir flask

# Expose the port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
