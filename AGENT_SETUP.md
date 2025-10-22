# AI Agent Deployment - Microsoft Agent Framework

## Overview

This deployment now includes **real AI agents** powered by the Microsoft Agent Framework:

- **Agent 1 (Developer-Agent)**: An autonomous software developer that can write, modify, and improve code
- **Agent 2 (CodeReview-Agent)**: A code review specialist that analyzes code for bugs, security issues, and quality improvements

Both agents use OpenAI GPT-4o-mini and have access to tools for file management, code analysis, and collaboration.

## Architecture

```
┌─────────────────────────────────────────────────┐
│            Exoscale VPS (Docker Host)           │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌─────────────────┐      ┌──────────────────┐ │
│  │  Developer-Agent│      │ CodeReview-Agent │ │
│  │   (Container 1) │      │   (Container 2)  │ │
│  │                 │      │                  │ │
│  │  - Write code   │      │  - Review code   │ │
│  │  - Create files │      │  - Find bugs     │ │
│  │  - Fix bugs     │      │  - Check quality │ │
│  │                 │      │  - Create reports│ │
│  └────────┬────────┘      └────────┬─────────┘ │
│           │                        │           │
│           └────────┬───────────────┘           │
│                    │                           │
│          ┌─────────▼──────────┐                │
│          │  Shared Workspace  │                │
│          │  /workspace/       │                │
│          │                    │                │
│          │  - Source code     │                │
│          │  - Projects        │                │
│          │  - Review reports  │                │
│          └────────────────────┘                │
│                                                 │
└─────────────────────────────────────────────────┘
```

## Agent Capabilities

### Developer-Agent

**Role**: Autonomous Software Developer

**Tools**:
- `read_file(file_path)` - Read files from workspace
- `write_file(file_path, content)` - Write/modify files
- `list_workspace_files()` - List all files
- `create_project_structure(name, type)` - Create new projects

**Initial Behavior**:
- Introduces itself
- Creates a sample "hello_world" Python project
- Waits for tasks in a loop (every 2 minutes)

**Approval Mode**: When `APPROVAL_REQUIRED=true`, the agent will log intended file changes but not execute them until approved.

### CodeReview-Agent

**Role**: Code Quality Assurance Specialist

**Tools**:
- `analyze_code_file(file_path)` - Deep code analysis
- `list_code_files(directory)` - Find code files
- `create_review_report(file, issues, suggestions)` - Generate review reports
- `check_code_quality_metrics(file_path)` - Calculate code metrics

**Initial Behavior**:
- Introduces itself and capabilities
- Scans workspace for code files
- Performs periodic reviews (every 5 minutes)
- Creates detailed review reports in `/workspace/code_reviews/`

## Quick Start

### 1. Stop Current Agents

```bash
cd /home/ubuntu/exoscale_deployment
docker-compose down
```

### 2. Rebuild with Microsoft Agent Framework

```bash
docker-compose build --no-cache
```

### 3. Start the AI Agents

```bash
docker-compose up -d
```

### 4. Watch the Agents Work

```bash
# Watch both agents
docker-compose logs -f

# Watch specific agent
docker-compose logs -f agent-1  # Developer Agent
docker-compose logs -f agent-2  # Code Review Agent
```

## Monitoring

### View Live Logs

```bash
# All agents
docker-compose logs -f

# Last 50 lines
docker-compose logs --tail=50

# Follow specific agent
docker-compose logs -f agent-1
```

### Check Agent Health

```bash
docker-compose ps
```

### Inspect Shared Workspace

```bash
ls -la /home/ubuntu/exoscale_deployment/shared/workspace/
```

### Check Review Reports

```bash
ls -la /home/ubuntu/exoscale_deployment/shared/workspace/code_reviews/
cat /home/ubuntu/exoscale_deployment/shared/workspace/code_reviews/review_*.md
```

## Configuration

### Environment Variables (.env file)

```bash
# API Keys
OPENAI_API_KEY=sk-proj-...         # ✓ Configured
ANTHROPIC_API_KEY=sk-ant-api03-... # ✓ Configured

# Optional: Azure OpenAI
AZURE_OPENAI_ENDPOINT=...
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_DEPLOYMENT_NAME=...
```

### Agent-Specific Settings

Edit `docker-compose.yml`:

```yaml
environment:
  - AGENT_NAME=Developer-Agent
  - AGENT_ROLE=developer
  - APPROVAL_REQUIRED=true  # Set to 'false' for full autonomy
```

## Transitioning to Full Autonomy

### Phase 1: Human-in-the-Loop (Current)

Both agents have `APPROVAL_REQUIRED=true`. They will:
- Analyze and plan changes
- Log what they would do
- Wait for human approval

### Phase 2: Semi-Autonomous

Set Developer Agent to autonomous:

```yaml
# In docker-compose.yml
agent-1:
  environment:
    - APPROVAL_REQUIRED=false  # Developer writes code automatically
```

Code Review Agent still requires approval.

### Phase 3: Fully Autonomous

Both agents autonomous:

```yaml
agent-1:
  environment:
    - APPROVAL_REQUIRED=false

agent-2:
  environment:
    - APPROVAL_REQUIRED=false
```

## Workflow Examples

### Example 1: Create a New Project

The Developer Agent will automatically create projects based on tasks. To give it a custom task, modify agent-1-code/main.py and change the `initial_task` variable.

### Example 2: Code Review Cycle

1. Developer Agent creates/modifies code
2. Code Review Agent detects new files (every 5 min)
3. Reviews are generated in `/workspace/code_reviews/`
4. Developer can read reviews and improve code

### Example 3: Collaborative Development

Both agents share the `/workspace` directory:
- Developer creates `project/main.py`
- Reviewer finds it and creates `code_reviews/review_main_*.md`
- Developer reads the review using `read_file` tool
- Developer updates code based on feedback

## Extending the System

### Add More Agents

1. Create new directory: `agent-3-code/`
2. Add service to `docker-compose.yml`
3. Write agent logic in `main.py`
4. Set role and tools

### Add Custom Tools

Edit `agent-X-code/main.py` and add new tool functions:

```python
def my_custom_tool(param: str) -> str:
    """Description of what this tool does."""
    # Implementation
    return result

# Add to agent tools list
agent = ChatAgent(
    ...
    tools=[..., my_custom_tool]
)
```

### Integrate with External Systems

- Add message queue (Redis, RabbitMQ)
- Connect to databases
- Integrate with CI/CD pipelines
- Add webhooks for GitHub/GitLab
- Connect to project management tools

## Troubleshooting

### Agent Not Starting

```bash
# Check logs
docker-compose logs agent-1

# Common issues:
# 1. Missing API key - check .env file
# 2. Build failed - run: docker-compose build --no-cache
# 3. Port conflicts - check: docker ps
```

### Agent Not Doing Anything

```bash
# Verify API key is loaded
docker exec agent-1 env | grep OPENAI_API_KEY

# Check if approval mode is blocking
docker exec agent-1 env | grep APPROVAL_REQUIRED
```

### Performance Issues

```bash
# Check resource usage
docker stats

# Increase limits in docker-compose.yml:
deploy:
  resources:
    limits:
      cpus: '2.0'
      memory: 2G
```

## Security Notes

- ✓ API keys stored in `.env` (file permissions: 600)
- ✓ `.env` added to `.gitignore`
- ✓ Agents run with resource limits
- ✓ Workspace isolated in Docker volumes
- ⚠️ Review all code changes before deploying to production
- ⚠️ Monitor agent behavior in approval mode first

## Next Steps

1. **Monitor** the agents for 24 hours in approval mode
2. **Review** the code they generate and the reviews they create
3. **Gradually increase autonomy** by setting APPROVAL_REQUIRED=false
4. **Add more specialized agents** (DevOps, Testing, Documentation)
5. **Implement workflow orchestration** using Microsoft Agent Framework workflows
6. **Add message queues** for agent communication
7. **Build a dashboard** using the DevUI package

## Resources

- [Microsoft Agent Framework Docs](https://learn.microsoft.com/agent-framework/)
- [Python Samples](https://github.com/microsoft/agent-framework/tree/main/python/samples)
- [Workflow Examples](https://github.com/microsoft/agent-framework/tree/main/python/samples/getting_started/workflows)
- [Agent Framework on GitHub](https://github.com/microsoft/agent-framework)

## Support

For issues:
1. Check agent logs: `docker-compose logs -f`
2. Review this documentation
3. Check Agent Framework GitHub issues
4. Examine the workspace: `/home/ubuntu/exoscale_deployment/shared/workspace/`

---

**Status**: ✅ Real AI agents deployed and running
**Framework**: Microsoft Agent Framework
**Model**: OpenAI GPT-4o-mini
**Mode**: Human-in-the-loop (APPROVAL_REQUIRED=true)
**Next**: Monitor and transition to autonomous operation
