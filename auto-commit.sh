#!/bin/bash
# Auto-commit script for agent code changes
# Usage: ./auto-commit.sh "commit message"

cd ~/exoscale_deployment

# Check if there are changes
if [[ -n $(git status -s) ]]; then
    echo "📝 Changes detected, creating backup commit..."
    git add .
    
    if [ -n "$1" ]; then
        git commit -m "[AUTO-COMMIT] $1"
    else
        git commit -m "[AUTO-COMMIT] Agent code changes at $(date)"
    fi
    
    echo "✅ Backup commit created: $(git log -1 --oneline)"
else
    echo "ℹ️  No changes to commit"
fi
