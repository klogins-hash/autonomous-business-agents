_# Exoscale Multi-Agent Deployment System

This package contains everything you need to deploy a multi-agent system on an Exoscale VPS. The system is designed for AI agents that can edit their own code, with a clear path to transition from human-supervised to fully autonomous operation.

## Project Structure

```
/exoscale_deployment
├── setup_vps.sh                # Script to create and configure the Exoscale VPS
├── docker-compose.yml          # Defines the agent services and their configurations
├── agent-image/                # Contains the base Docker image for all agents
│   ├── Dockerfile              # Builds the agent's container environment
│   └── main.py                 # Placeholder for the agent's core logic
├── agent-1-code/               # Code specific to Agent 1 (mounted into its container)
│   └── agent.py
├── agent-2-code/               # Code specific to Agent 2 (mounted into its container)
│   └── agent.py
├── shared/
│   └── logs/                   # Shared directory for logs from all agents
└── README.md                   # This file
```

## How It Works

1.  **`setup_vps.sh`**: This script automates the creation of a secure Exoscale compute instance. It installs the Exoscale CLI, sets up SSH keys and firewall rules, and creates a new VPS with Docker pre-installed.

2.  **Docker & Docker Compose**: The system uses Docker to isolate each agent in its own container. `docker-compose.yml` orchestrates the multi-agent setup, making it easy to start, stop, and manage all agents with a single command.

3.  **Mounted Code Volumes**: Each agent's code is stored on the host machine (in `agent-1-code/`, `agent-2-code/`, etc.) and mounted as a volume into its respective container. This means:
    *   **Agents can edit their own code**: Any changes an agent makes to files in its `/app` directory are reflected immediately on the host machine.
    *   **Code is persistent**: Code changes survive container restarts and server reboots.

4.  **Human Oversight → Autonomous Transition**: The `APPROVAL_REQUIRED` environment variable in `docker-compose.yml` allows you to control the agents' autonomy. 
    *   `true`: The agent will perform its task and then wait for external approval before making changes (human oversight).
    *   `false`: The agent will perform its task and then autonomously proceed to modify its code.

## Deployment Guide

A full, step-by-step deployment guide is provided in `deployment_guide.md`.

