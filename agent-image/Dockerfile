# Dockerfile for the AI Agent
# This defines the base image and environment for your agents.

FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Microsoft Agent Framework and dependencies
RUN pip install --no-cache-dir \
    agent-framework --pre \
    openai \
    anthropic \
    python-dotenv \
    aiohttp

# Copy the agent code into the container
COPY main.py ./

# Set the entrypoint
CMD ["python", "main.py"]

