
# ---- Python Build Stage ----
FROM python:3.11-alpine3.17 AS python-builder
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy Python script
COPY create_mapping.py .

# ---- Elasticsearch Image ----
FROM docker.elastic.co/elasticsearch/elasticsearch:8.9.0

# Install python3 and pip
USER root
RUN apt-get update && apt-get install -y python3 python3-pip

# Copy Python script from builder image
COPY --from=python-builder /app/create_mapping.py /usr/local/bin/create_mapping.py

# Copy requirements and install Python dependencies
COPY --from=python-builder /app/requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# Make script executable
RUN chmod +x /usr/local/bin/create_mapping.py

# Switch back to elasticsearch user
USER elasticsearch

# Run the Python script in the background and then start Elasticsearch
CMD ["sh", "-c", "python3 /usr/local/bin/create_mapping.py & /usr/local/bin/docker-entrypoint.sh"]
