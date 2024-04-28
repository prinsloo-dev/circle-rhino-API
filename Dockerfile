# Use the official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install necessary packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    openssh-client git gcc python3-dev build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create SSH directory
RUN mkdir -p /root/.ssh/

# Copy SSH private key
ARG SSH_PRIVATE_KEY
RUN echo "${SSH_PRIVATE_KEY}" >> /root/.ssh/id_ed25519 && \
    chmod 600 /root/.ssh/id_ed25519 && \
    touch /root/.ssh/known_hosts && \
    ssh-keyscan gitlab.com >> /root/.ssh/known_hosts

# Copy source code
COPY requirements.txt requirements.txt
COPY . .

# Install Python dependencies
RUN pip install -U pip \
    pip install --upgrade pip setuptools && \
    pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=src/app.py
ENV FLASK_RUN_HOST=0.0.0.0


# Run Flask app with a non-root user
RUN groupadd -r myuser && useradd -r -g myuser myuser
USER myuser

CMD ["flask", "run"]
