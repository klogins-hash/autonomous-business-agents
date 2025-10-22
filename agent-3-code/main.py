"""
Magentic Manager Agent - Orchestrates Developer and Code Review Agents
This is the "brain" that coordinates all agents to complete complex business tasks
"""

import os
import asyncio
import logging
from datetime import datetime
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(name)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger("Magentic-Manager")


async def main():
    """Main orchestration loop."""
    agent_name = os.getenv("AGENT_NAME", "Magentic-Manager")

    try:
        # Import Agent Framework components
        from agent_framework import (
            ChatAgent,
            MagenticBuilder,
            MagenticCallbackEvent,
            MagenticCallbackMode,
            MagenticOrchestratorMessageEvent,
            MagenticAgentDeltaEvent,
            MagenticAgentMessageEvent,
            MagenticFinalResultEvent,
            WorkflowOutputEvent,
        )
        from agent_framework.openai import OpenAIChatClient

        logger.info(f"{agent_name} starting up with Microsoft Agent Framework...")

        # Check for API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.error("OPENAI_API_KEY not set! Agent cannot function without API key.")
            logger.info("Falling back to basic loop mode...")

            while True:
                logger.info(f"{agent_name} is running (waiting for API key configuration)")
                await asyncio.sleep(60)
            return

        # Create specialized agents that Magentic will coordinate
        # These agents work together as a complete development team

        developer_agent = ChatAgent(
            name="DeveloperAgent",
            description="Expert software developer - implements features and writes code",
            instructions="""You are an expert software developer. Your role is to:
1. Write clean, well-documented code
2. Implement features based on requirements
3. Fix bugs and improve code quality
4. Create project structures

You focus on implementation and getting things working. You are in AUTONOMOUS mode.""",
            chat_client=OpenAIChatClient(),
        )

        reviewer_agent = ChatAgent(
            name="ReviewerAgent",
            description="Code quality expert - reviews code for bugs and improvements",
            instructions="""You are a code review specialist. Your role is to:
1. Review code for bugs and security issues
2. Suggest improvements and best practices
3. Check code quality and readability
4. Provide constructive feedback

You focus on quality, security, and maintainability.""",
            chat_client=OpenAIChatClient(),
        )

        devops_agent = ChatAgent(
            name="DevOpsAgent",
            description="Infrastructure and deployment specialist - handles CI/CD and deployments",
            instructions="""You are a DevOps engineer. Your role is to:
1. Deploy applications safely to production
2. Manage CI/CD pipelines
3. Monitor system health
4. Handle scaling and infrastructure

You focus on reliability, deployment safety, and system health.""",
            chat_client=OpenAIChatClient(),
        )

        qa_agent = ChatAgent(
            name="QAAgent",
            description="Quality assurance and testing expert - ensures code quality through testing",
            instructions="""You are a QA and testing specialist. Your role is to:
1. Write comprehensive test suites
2. Run tests and report results
3. Check code coverage
4. Perform load and performance testing

You focus on quality, test coverage, and reliability.""",
            chat_client=OpenAIChatClient(),
        )

        monitoring_agent = ChatAgent(
            name="MonitoringAgent",
            description="Monitoring and metrics specialist - tracks performance and provides insights",
            instructions="""You are a monitoring and analytics expert. Your role is to:
1. Generate dashboards and reports
2. Collect performance metrics
3. Identify bottlenecks and issues
4. Provide business intelligence

You focus on visibility, metrics, and insights.""",
            chat_client=OpenAIChatClient(),
        )

        # Callback to handle workflow events
        last_stream_agent_id = None
        stream_line_open = False

        async def on_event(event: MagenticCallbackEvent) -> None:
            """Handle events from the Magentic workflow."""
            nonlocal last_stream_agent_id, stream_line_open

            if isinstance(event, MagenticOrchestratorMessageEvent):
                logger.info(f"[MANAGER-{event.kind}] {getattr(event.message, 'text', '')}")
                print(f"\n🧠 MANAGER [{event.kind}]:")
                print(f"{getattr(event.message, 'text', '')}")
                print("-" * 60)

            elif isinstance(event, MagenticAgentDeltaEvent):
                # Streaming output from agents
                if last_stream_agent_id != event.agent_id or not stream_line_open:
                    if stream_line_open:
                        print()
                    agent_emoji = "👨‍💻" if "Developer" in event.agent_id else "🔍"
                    print(f"\n{agent_emoji} {event.agent_id}: ", end="", flush=True)
                    last_stream_agent_id = event.agent_id
                    stream_line_open = True
                print(event.text, end="", flush=True)

            elif isinstance(event, MagenticAgentMessageEvent):
                if stream_line_open:
                    print()
                    stream_line_open = False
                msg = event.message
                if msg is not None:
                    logger.info(f"[{event.agent_id}] Completed: {msg.text[:100]}...")

            elif isinstance(event, MagenticFinalResultEvent):
                print("\n" + "=" * 60)
                print("✅ FINAL RESULT")
                print("=" * 60)
                if event.message is not None:
                    print(event.message.text)
                print("=" * 60)

        # Build the Magentic workflow with ALL 5 specialist agents
        logger.info("Building Magentic workflow with 5-agent team...")

        workflow = (
            MagenticBuilder()
            .participants(
                developer=developer_agent,
                reviewer=reviewer_agent,
                devops=devops_agent,
                qa=qa_agent,
                monitoring=monitoring_agent
            )
            .on_event(on_event, mode=MagenticCallbackMode.STREAMING)
            .with_standard_manager(
                chat_client=OpenAIChatClient(),
                max_round_count=15,  # More rounds for complex multi-agent tasks
                max_stall_count=4,   # Allow more stalls with more agents
                max_reset_count=3,   # More resets for reliability
            )
            .build()
        )

        logger.info("✅ Magentic workflow initialized successfully")
        logger.info("Full Team Available:")
        logger.info("  👨‍💻 DeveloperAgent (Autonomous)")
        logger.info("  🔍 ReviewerAgent")
        logger.info("  🚀 DevOpsAgent")
        logger.info("  🧪 QAAgent")
        logger.info("  📊 MonitoringAgent")

        # Example tasks demonstrating full-stack Magentic orchestration
        tasks = [
            {
                "name": "Build Complete Feature",
                "description": """Build a complete user authentication system with full quality checks:
1. Developer: Create user registration and login functions
2. Reviewer: Security audit the authentication code
3. QA: Write unit tests and verify >85% coverage
4. Developer: Fix any issues found
5. Monitoring: Generate quality metrics report"""
            },
            {
                "name": "Deploy with Full Pipeline",
                "description": """Take the authentication system through full deployment:
1. QA: Run complete test suite
2. Reviewer: Final code review
3. DevOps: Create deployment plan
4. Monitoring: Set up health checks and alerts"""
            }
        ]

        # Task execution loop
        task_interval = 300  # Run a task every 5 minutes

        for task_idx, task in enumerate(tasks):
            logger.info(f"\n{'='*60}")
            logger.info(f"TASK #{task_idx + 1}: {task['name']}")
            logger.info(f"{'='*60}")

            print(f"\n\n📋 TASK: {task['name']}")
            print(f"Description: {task['description']}")
            print("\n" + "=" * 60)

            try:
                output = None
                async for event in workflow.run_stream(task['description']):
                    if isinstance(event, WorkflowOutputEvent):
                        output = str(event.data)

                if output:
                    logger.info(f"Task completed successfully")
                    print(f"\n📊 Workflow Output:\n{output}")
                else:
                    logger.warning("Task completed but no output received")

            except Exception as e:
                logger.error(f"Task failed: {e}", exc_info=True)
                print(f"\n❌ Task failed: {e}")

            # Wait before next task
            if task_idx < len(tasks) - 1:
                logger.info(f"Waiting {task_interval}s before next task...")
                await asyncio.sleep(task_interval)

        # Main monitoring loop
        logger.info("\n" + "="*60)
        logger.info("All initial tasks completed. Entering monitoring mode...")
        logger.info("="*60)

        while True:
            logger.info("Magentic Manager is active and monitoring...")
            logger.info("In production, this would:")
            logger.info("  - Pull tasks from a message queue")
            logger.info("  - Coordinate agent-to-agent communication")
            logger.info("  - Monitor agent health and performance")
            logger.info("  - Handle failures and retries")
            logger.info("  - Report metrics to a dashboard")

            await asyncio.sleep(120)

    except ImportError as e:
        logger.error(f"Failed to import Agent Framework: {e}")
        logger.error("Make sure agent-framework is installed")

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
        logger.info("Magentic Manager shutting down...")
