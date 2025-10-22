"""
Developer Agent - Uses Microsoft Agent Framework
This agent can write, modify, and improve code autonomously
"""

import os
import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(name)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger("Developer-Agent")


def read_file(file_path: str) -> str:
    """Read a file from the workspace.

    Args:
        file_path: Path to the file to read

    Returns:
        The contents of the file
    """
    try:
        workspace = Path("/workspace")
        full_path = workspace / file_path

        if not full_path.exists():
            return f"Error: File '{file_path}' not found in workspace"

        with open(full_path, 'r') as f:
            content = f.read()

        logger.info(f"Read file: {file_path} ({len(content)} chars)")
        return content
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        return f"Error reading file: {str(e)}"


def write_file(file_path: str, content: str) -> str:
    """Write content to a file in the workspace.

    Args:
        file_path: Path to the file to write
        content: Content to write to the file

    Returns:
        Success or error message
    """
    try:
        workspace = Path("/workspace")
        full_path = workspace / file_path

        # Create parent directories if they don't exist
        full_path.parent.mkdir(parents=True, exist_ok=True)

        # Check if approval is required
        approval_required = os.getenv("APPROVAL_REQUIRED", "true").lower() == "true"

        if approval_required:
            logger.info(f"Would write to {file_path} ({len(content)} chars) - APPROVAL REQUIRED")
            return f"File modification requires approval. Would write {len(content)} chars to '{file_path}'"
        else:
            with open(full_path, 'w') as f:
                f.write(content)
            logger.info(f"Wrote file: {file_path} ({len(content)} chars)")
            return f"Successfully wrote {len(content)} characters to '{file_path}'"

    except Exception as e:
        logger.error(f"Error writing file {file_path}: {e}")
        return f"Error writing file: {str(e)}"


def list_workspace_files() -> str:
    """List all files in the workspace.

    Returns:
        List of files in the workspace
    """
    try:
        workspace = Path("/workspace")
        workspace.mkdir(exist_ok=True)

        files = []
        for item in workspace.rglob("*"):
            if item.is_file():
                rel_path = item.relative_to(workspace)
                files.append(str(rel_path))

        if files:
            logger.info(f"Found {len(files)} files in workspace")
            return f"Files in workspace:\n" + "\n".join(f"  - {f}" for f in sorted(files))
        else:
            return "Workspace is empty"
    except Exception as e:
        logger.error(f"Error listing workspace: {e}")
        return f"Error listing workspace: {str(e)}"


def create_project_structure(project_name: str, project_type: str = "python") -> str:
    """Create a new project structure in the workspace.

    Args:
        project_name: Name of the project
        project_type: Type of project (python, javascript, etc.)

    Returns:
        Success message
    """
    try:
        workspace = Path("/workspace")
        project_path = workspace / project_name

        if project_path.exists():
            return f"Error: Project '{project_name}' already exists"

        # Create project structure based on type
        if project_type == "python":
            (project_path / "src").mkdir(parents=True)
            (project_path / "tests").mkdir(parents=True)
            (project_path / "docs").mkdir(parents=True)

            # Create initial files
            (project_path / "README.md").write_text(f"# {project_name}\n\nA new Python project.\n")
            (project_path / "requirements.txt").write_text("")
            (project_path / ".gitignore").write_text("__pycache__/\n*.pyc\n.env\nvenv/\n")

        logger.info(f"Created {project_type} project: {project_name}")
        return f"Successfully created {project_type} project '{project_name}'"

    except Exception as e:
        logger.error(f"Error creating project: {e}")
        return f"Error creating project: {str(e)}"


async def main():
    """Main agent loop."""
    agent_name = os.getenv("AGENT_NAME", "Developer-Agent")

    try:
        # Import Agent Framework components
        from agent_framework.openai import OpenAIChatClient
        from agent_framework import ChatAgent

        logger.info(f"{agent_name} starting up with Microsoft Agent Framework...")

        # Check for API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.error("OPENAI_API_KEY not set! Agent cannot function without API key.")
            logger.info("Falling back to basic loop mode...")

            # Fallback mode - just log status
            while True:
                logger.info(f"{agent_name} is running (waiting for API key configuration)")
                await asyncio.sleep(60)
            return

        # Create the Developer Agent with tools
        # OpenAIChatClient reads from OPENAI_API_KEY environment variable
        agent = OpenAIChatClient().create_agent(
            name=agent_name,
            instructions="""You are an expert software developer agent. Your role is to:

1. Write clean, well-documented code
2. Create project structures and organize code properly
3. Implement features based on requirements
4. Fix bugs and improve code quality
5. Follow best practices and coding standards

You have access to tools to read, write, and manage files in a workspace.
When writing code, always include comments and documentation.
Be proactive in creating complete, working solutions.

Current workspace: /workspace/
""",
            tools=[
                read_file,
                write_file,
                list_workspace_files,
                create_project_structure
            ]
        )

        logger.info(f"{agent_name} initialized successfully with OpenAI GPT-4")
        logger.info("Available tools: read_file, write_file, list_workspace_files, create_project_structure")

        # Task queue - in a real system, this would come from a message queue
        task_interval = 120  # Check for tasks every 2 minutes

        # Initial task: Introduce yourself and create a sample project
        initial_task = """Hello! Please introduce yourself and then create a simple Python project called 'hello_world'
        with a main.py file that prints 'Hello from the Developer Agent!'."""

        logger.info("Running initial task...")
        try:
            result = await agent.run(initial_task)
            logger.info(f"Agent response:\n{result}")
        except Exception as e:
            logger.error(f"Error running initial task: {e}")

        # Main loop - wait for tasks
        task_count = 0
        while True:
            task_count += 1
            logger.info(f"Waiting for next task... (task #{task_count} completed)")
            logger.info(f"Workspace status: {list_workspace_files()}")

            await asyncio.sleep(task_interval)

            # In production, you would:
            # 1. Pull tasks from a message queue
            # 2. Process them with the agent
            # 3. Report results back

    except ImportError as e:
        logger.error(f"Failed to import Agent Framework: {e}")
        logger.error("Make sure agent-framework is installed")

        # Fallback mode
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
        logger.info("Agent shutting down...")
