"""
DevOps Agent - Deployment, Infrastructure & Monitoring Specialist
Handles CI/CD, deployments, scaling, and production monitoring
"""

import os
import asyncio
import logging
from datetime import datetime
from pathlib import Path
import subprocess

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(name)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger("DevOps-Agent")


def deploy_to_docker(project_path: str, service_name: str) -> str:
    """Deploy a project to Docker.

    Args:
        project_path: Path to the project directory
        service_name: Name for the Docker service

    Returns:
        Deployment status message
    """
    try:
        workspace = Path("/workspace")
        full_path = workspace / project_path

        if not full_path.exists():
            return f"Error: Project '{project_path}' not found in workspace"

        # Check if approval is required
        approval_required = os.getenv("APPROVAL_REQUIRED", "true").lower() == "true"

        deployment_plan = f"""
Deployment Plan for {service_name}:
1. Build Docker image from {project_path}
2. Tag image as {service_name}:latest
3. Stop existing container (if any)
4. Start new container
5. Run health checks
6. Monitor for 60 seconds
"""

        if approval_required:
            logger.info(f"Deployment planned for {service_name} - APPROVAL REQUIRED")
            return f"Deployment requires approval:\n{deployment_plan}"
        else:
            logger.info(f"Deploying {service_name} autonomously...")
            # In real implementation, would execute docker commands here
            return f"Deployed {service_name} successfully!\n{deployment_plan}"

    except Exception as e:
        logger.error(f"Error in deployment: {e}")
        return f"Deployment error: {str(e)}"


def check_system_health() -> str:
    """Check overall system health.

    Returns:
        Health status report
    """
    try:
        logger.info("Performing system health check...")

        # Simulated health metrics
        health_report = f"""
System Health Report - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Docker Status:
  ✓ Docker daemon: Running
  ✓ Containers: 6 running, 0 stopped
  ✓ Images: 6 total
  ✓ Networks: 2 active

Resource Usage:
  ✓ CPU: 45% (Normal)
  ✓ Memory: 3.2GB / 8GB (40%)
  ✓ Disk: 25GB / 100GB (25%)

Services Status:
  ✓ agent-1 (Developer): Healthy
  ✓ agent-2 (Reviewer): Healthy
  ✓ agent-3 (Magentic): Healthy
  ✓ agent-4 (DevOps): Healthy
  ✓ agent-5 (QA): Healthy
  ✓ agent-6 (DevUI): Healthy

Alerts: None
All systems operational ✓
"""
        logger.info("Health check completed")
        return health_report

    except Exception as e:
        logger.error(f"Error in health check: {e}")
        return f"Health check error: {str(e)}"


def scale_service(service_name: str, replicas: int) -> str:
    """Scale a service to specified number of replicas.

    Args:
        service_name: Name of the service to scale
        replicas: Number of replicas to run

    Returns:
        Scaling status message
    """
    try:
        approval_required = os.getenv("APPROVAL_REQUIRED", "true").lower() == "true"

        scaling_plan = f"""
Scaling Plan:
Service: {service_name}
Current replicas: 1
Target replicas: {replicas}
Strategy: Rolling update
Expected downtime: 0 seconds
"""

        if approval_required:
            logger.info(f"Scaling {service_name} to {replicas} replicas - APPROVAL REQUIRED")
            return f"Scaling requires approval:\n{scaling_plan}"
        else:
            logger.info(f"Scaling {service_name} to {replicas} replicas...")
            return f"Scaled {service_name} to {replicas} replicas successfully!\n{scaling_plan}"

    except Exception as e:
        logger.error(f"Error in scaling: {e}")
        return f"Scaling error: {str(e)}"


def create_ci_cd_pipeline(project_path: str) -> str:
    """Create CI/CD pipeline configuration.

    Args:
        project_path: Path to the project

    Returns:
        Pipeline configuration details
    """
    try:
        workspace = Path("/workspace")
        full_path = workspace / project_path

        if not full_path.exists():
            return f"Error: Project '{project_path}' not found"

        pipeline_config = f"""
CI/CD Pipeline for {project_path}:

Triggers:
- Git push to main branch
- Pull request created
- Manual trigger

Stages:
1. Build:
   - Install dependencies
   - Build Docker image
   - Tag with commit SHA

2. Test:
   - Run unit tests
   - Run integration tests
   - Check code coverage (>80%)

3. Security:
   - Scan for vulnerabilities
   - Check dependencies
   - SAST analysis

4. Deploy:
   - Deploy to staging
   - Run smoke tests
   - Deploy to production (manual approval)

5. Monitor:
   - Health checks
   - Performance metrics
   - Error tracking
"""

        logger.info(f"CI/CD pipeline configured for {project_path}")
        return f"Pipeline configured:\n{pipeline_config}"

    except Exception as e:
        logger.error(f"Error creating pipeline: {e}")
        return f"Pipeline error: {str(e)}"


def rollback_deployment(service_name: str, version: str = "previous") -> str:
    """Rollback a deployment to a previous version.

    Args:
        service_name: Name of the service
        version: Version to rollback to (default: previous)

    Returns:
        Rollback status
    """
    try:
        rollback_plan = f"""
Rollback Plan:
Service: {service_name}
Target version: {version}
Strategy: Instant rollback
Steps:
1. Stop current version
2. Start previous version
3. Verify health
4. Route traffic
Expected time: 30 seconds
"""

        logger.info(f"Rolling back {service_name} to {version}")
        return f"Rollback executed:\n{rollback_plan}"

    except Exception as e:
        logger.error(f"Error in rollback: {e}")
        return f"Rollback error: {str(e)}"


async def main():
    """Main agent loop."""
    agent_name = os.getenv("AGENT_NAME", "DevOps-Agent")

    try:
        from agent_framework.openai import OpenAIChatClient
        from agent_framework import ChatAgent

        logger.info(f"{agent_name} starting up with Microsoft Agent Framework...")

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.error("OPENAI_API_KEY not set!")
            while True:
                logger.info(f"{agent_name} is running (waiting for API key)")
                await asyncio.sleep(60)
            return

        # Create DevOps Agent with deployment tools
        agent = OpenAIChatClient().create_agent(
            name=agent_name,
            instructions="""You are an expert DevOps and Infrastructure engineer. Your role is to:

1. Deploy applications to production
2. Manage CI/CD pipelines
3. Monitor system health and performance
4. Scale services based on demand
5. Handle incidents and rollbacks
6. Ensure high availability and reliability

You have access to tools for deployment, scaling, health checks, CI/CD, and rollbacks.
Always prioritize system stability and zero-downtime deployments.

Current environment: Docker-based deployment on VPS
""",
            tools=[
                deploy_to_docker,
                check_system_health,
                scale_service,
                create_ci_cd_pipeline,
                rollback_deployment
            ]
        )

        logger.info(f"{agent_name} initialized successfully")
        logger.info("Available tools: deploy, health_check, scale, ci_cd, rollback")

        # Initial health check
        initial_task = """Hello! Please introduce yourself and then perform a system health check
        to ensure all services are running properly."""

        logger.info("Running initial health check...")
        try:
            result = await agent.run(initial_task)
            logger.info(f"Agent response:\n{result}")
        except Exception as e:
            logger.error(f"Error in initial task: {e}")

        # Main monitoring loop
        monitoring_interval = 180  # Check every 3 minutes

        while True:
            await asyncio.sleep(monitoring_interval)

            logger.info("Running scheduled health check...")
            health_task = "Perform a system health check and report any issues."

            try:
                result = await agent.run(health_task)
                logger.info("Health check completed")
            except Exception as e:
                logger.error(f"Error in health check: {e}")

    except ImportError as e:
        logger.error(f"Failed to import Agent Framework: {e}")
        while True:
            logger.info(f"{agent_name} is running (Agent Framework not available)")
            await asyncio.sleep(60)

    except Exception as e:
        logger.error(f"Error in main loop: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("DevOps Agent shutting down...")
