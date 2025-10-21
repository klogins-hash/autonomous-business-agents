# Dockerfile for the AI Agent
# This defines the base image and environment for your agents.

FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir requests

# Copy the agent code into the container
COPY main.py ./

# Set the entrypoint
CMD ["python", "main.py"]

