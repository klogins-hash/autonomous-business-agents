# Quick Reference Guide
## Autonomous Business Agent System - Daily Operations

---

## System Status At A Glance

**Quick Status Check**:
```bash
docker-compose ps
```

Expected output: All 6 agents showing "Up" and "healthy"

---

## Common Commands

### Starting & Stopping

```bash
# Start all agents
docker-compose up -d

# Stop all agents gracefully
docker-compose down

# Restart specific agent
docker-compose restart agent-1

# Rebuild and restart (after code changes)
docker-compose down && docker-compose build --no-cache && docker-compose up -d
```

### Monitoring

```bash
# View all logs (live)
docker-compose logs -f

# View specific agent logs
docker-compose logs -f agent-1  # Developer (Semi-Autonomous)
docker-compose logs -f agent-3  # Magentic Manager (Orchestrator)
docker-compose logs -f agent-6  # DevUI Dashboard

# View last 100 lines
docker-compose logs --tail=100

# View logs for specific time
docker-compose logs --since 10m  # Last 10 minutes
```

### System Health

```bash
# Check container status
docker-compose ps

# Check resource usage
docker stats

# Check workspace files
ls -la shared/workspace/

# Check logs directory
ls -la shared/logs/
```

---

## Agent Quick Reference

| ID | Name | Role | Autonomy | When to Use |
|----|------|------|----------|-------------|
| **agent-1** | Developer | Code writer | ⚡ Semi-Auto | Any coding task |
| **agent-2** | Reviewer | Code review | 🤚 Manual | Security audits |
| **agent-3** | Magentic | Orchestrator | 🤚 Manual | Complex multi-step tasks |
| **agent-4** | DevOps | Deploy/Infra | 🤚 Manual | Deployments, scaling |
| **agent-5** | QA | Testing | 🤚 Manual | Test coverage, quality |
| **agent-6** | DevUI | Monitoring | 🤚 Manual | Dashboards, metrics |

---

## What's Running Right Now?

```bash
# See what each agent is doing
docker-compose logs --tail=20 agent-1  # Latest Developer actions
docker-compose logs --tail=20 agent-3  # Current Magentic task
docker-compose logs --tail=20 agent-6  # Latest dashboard
```

---

## Autonomous vs Manual Agents

### ⚡ Semi-Autonomous (No Approval Needed)
- **agent-1 (Developer)**
  - Automatically creates files
  - Automatically writes code
  - Automatically structures projects
  - **View activity**: `docker-compose logs -f agent-1`

### 🤚 Manual Approval Required
- **agent-2, agent-3, agent-4, agent-5, agent-6**
  - Wait for task injection
  - Execute when Magentic delegates
  - Require approval for standalone tasks

---

## Enabling More Autonomy

**To make any agent autonomous**, edit `docker-compose.yml`:

```yaml
agent-X:
  environment:
    - APPROVAL_REQUIRED=false  # ← Change to false
```

Then restart:
```bash
docker-compose down && docker-compose up -d
```

**Recommended next autonomy**: agent-5 (QA) and agent-6 (DevUI)

---

## Watching Magentic Orchestration

Magentic Manager coordinates multi-agent workflows. Watch it in action:

```bash
docker-compose logs -f agent-3
```

You'll see:
```
[MANAGER-TextMessage] Analyzing task...
[DeveloperAgent] Implementing feature...
[ReviewerAgent] Security audit complete...
[QAAgent] Tests written, coverage: 91%
[FINAL RESULT] Task complete!
```

---

## Current System State

**As of last deployment**:
- ✅ All 6 agents running and healthy
- ✅ Developer Agent creating code autonomously
- ✅ Magentic Manager orchestrating authentication system task
- ✅ DevUI Dashboard updating every 60 seconds
- ✅ Shared workspace active with 4 files

**Check current workspace**:
```bash
tree shared/workspace/
```

---

## Troubleshooting

### Agent keeps restarting
```bash
# Check logs for errors
docker-compose logs agent-X

# Rebuild if needed
docker-compose down
docker-compose build --no-cache agent-X
docker-compose up -d
```

### Can't see agent output
```bash
# Make sure container is running
docker-compose ps

# Check if healthy
docker inspect agent-X | grep Health
```

### High API costs
```bash
# Count API calls in last hour
docker-compose logs --since 1h | grep "api.openai.com" | wc -l

# Stop non-essential agents
docker-compose stop agent-6  # Monitoring
```

### Need to reset everything
```bash
# Nuclear option - complete reset
docker-compose down -v  # Removes volumes too
docker-compose build --no-cache
docker-compose up -d
```

---

## Daily Checklist

### Morning Startup
```bash
# 1. Start system
docker-compose up -d

# 2. Verify all agents healthy
docker-compose ps

# 3. Check overnight activity
docker-compose logs --since 12h | grep "completed"

# 4. View current workspace
ls -la shared/workspace/
```

### During Day
```bash
# Monitor Magentic orchestration
docker-compose logs -f agent-3

# Check Developer autonomous actions
docker-compose logs -f agent-1

# View real-time dashboard
docker-compose logs -f agent-6
```

### End of Day
```bash
# 1. Review completed tasks
docker-compose logs | grep "completed"

# 2. Check resource usage
docker stats --no-stream

# 3. Backup workspace
tar -czf workspace-backup-$(date +%Y%m%d).tar.gz shared/workspace/

# 4. Optional: Stop system
docker-compose down
```

---

## Environment Configuration

**File**: `.env`

```bash
# Required
OPENAI_API_KEY=sk-proj-...
OPENAI_CHAT_MODEL_ID=gpt-4o-mini

# Optional
ANTHROPIC_API_KEY=sk-ant-...
```

**Update after .env changes**:
```bash
docker-compose down && docker-compose up -d
```

---

## Resource Limits

**Current Allocation**:
- Total: 5.5 CPU cores, 6.5GB RAM
- agent-3 (Magentic): 1.5 CPU, 2GB (largest)
- Others: 0.5-1.0 CPU, 512MB-1GB

**Monitor usage**:
```bash
docker stats
```

**Adjust in `docker-compose.yml`** if needed:
```yaml
deploy:
  resources:
    limits:
      cpus: '2.0'
      memory: 2G
```

---

## File Locations

```
/home/ubuntu/exoscale_deployment/
├── .env                          # API keys
├── docker-compose.yml            # Agent configuration
├── agent-image/
│   ├── Dockerfile               # Base image
│   └── main.py                  # Placeholder (not used)
├── agent-1-code/main.py         # Developer Agent
├── agent-2-code/main.py         # Reviewer Agent
├── agent-3-code/main.py         # Magentic Manager
├── agent-4-code/main.py         # DevOps Agent
├── agent-5-code/main.py         # QA Agent
├── agent-6-code/main.py         # DevUI Agent
├── shared/
│   ├── workspace/               # Agent collaboration space
│   └── logs/                    # Centralized logs
└── *.md                         # Documentation
```

---

## Emergency Commands

### Agent consuming too much CPU
```bash
docker-compose restart agent-X
```

### System unresponsive
```bash
docker-compose down -t 0  # Force stop
docker-compose up -d
```

### Out of disk space
```bash
# Clean Docker
docker system prune -a

# Clean logs
rm -rf shared/logs/*.log
```

### API quota exceeded
```bash
# Stop all agents immediately
docker-compose down

# Check .env for API key
cat .env | grep OPENAI_API_KEY

# Check OpenAI account at https://platform.openai.com/account/usage
```

---

## Next Steps

**Immediate**:
1. Watch Magentic complete current task: `docker-compose logs -f agent-3`
2. Review Developer autonomous work: `ls -la shared/workspace/`
3. Check DevUI dashboard: `docker-compose logs agent-6 | tail -100`

**This Week**:
1. Enable QA Agent autonomy
2. Enable DevUI Agent autonomy
3. Add Slack notifications
4. Implement task queue

**This Month**:
1. Add Business Logic Agent
2. Create customer-facing API
3. Set up GitHub integration
4. Full CI/CD pipeline

---

## Getting Help

**View Documentation**:
```bash
ls -la *.md

# Quick start
cat QUICK_REFERENCE.md

# Complete guide
cat COMPLETE_SYSTEM_GUIDE.md

# Agent-specific
cat AGENT_SETUP.md

# Magentic deep dive
cat MAGENTIC_GUIDE.md
```

**Check System Health**:
```bash
# One-liner health check
docker-compose ps && echo "---" && docker stats --no-stream && echo "---" && ls shared/workspace/
```

---

**Version**: 1.0.0
**Last Updated**: October 22, 2025
