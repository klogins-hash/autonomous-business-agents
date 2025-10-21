# Claude Code on VPS - Complete Setup Guide

## ✅ What's Installed

- **Claude Code v2.0.24** - Latest version installed globally
- **Node.js v20.19.5** - Runtime environment  
- **Git** - Version control configured
- **Docker & Docker Compose** - Container management
- **Full system access** - Claude Code can manage everything

## 🚀 Quick Start

### 1. Set Your API Key

```bash
export ANTHROPIC_API_KEY='your-api-key-here'
echo 'export ANTHROPIC_API_KEY=your-api-key-here' >> ~/.bashrc
source ~/.bashrc
```

### 2. Launch Claude Code

```bash
cd ~/exoscale_deployment
claude
```

### 3. Or Use Inline Commands

```bash
claude 'show me the agent logs'
claude 'improve the agent code to handle errors better'
```

## 🎯 What Claude Code Can Do

- View and analyze agent logs
- Modify agent code and restart services
- Debug issues and add new features
- Git operations and Docker management
- Full development workflows

## 📋 Common Commands

```bash
# Check agent status
claude 'check all agent logs and health'

# Modify code
claude 'update agent-1 to handle errors better'

# Deploy changes
claude 'commit changes and restart agents'
```

## 🔧 Configuration

**Config**: `~/.config/claude-code/config.json`
**Workspace**: `/home/ubuntu/exoscale_deployment`

## 🛡️ Security

- Git auto-backup with `./auto-commit.sh`
- Resource limits: 0.5 CPU, 512MB RAM per agent
- Health checks enabled
- No sudo access (by design)

## 🆘 Emergency Commands

```bash
docker-compose stop           # Stop all
docker-compose restart        # Restart all
git reset --hard HEAD~1       # Rollback
docker exec -it agent-1 bash  # Shell access
```
