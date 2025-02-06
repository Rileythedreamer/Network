FROM mcr.microsoft.com/devcontainers/python:3.9

# Install the PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /workspace
