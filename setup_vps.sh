#!/bin/bash

# Exoscale VPS Setup Script
# This script automates the creation of a new compute instance on Exoscale,
# configured for a multi-agent Docker deployment.

# --- Configuration ---
# You can modify these variables
INSTANCE_NAME="ai-agent-host-01"
INSTANCE_TYPE="standard.medium" # 4GB RAM, 2 Cores - good for 3-5 agents
DISK_SIZE=80 # GB
ZONE="de-fra-1" # Frankfurt, Germany - good for US connectivity
TEMPLATE_NAME="Linux Ubuntu 22.04 LTS 64-bit"
SSH_KEY_NAME="agent-vps-key"
SECURITY_GROUP_NAME="agent-host-sg"

# --- Exoscale API Credentials (from user) ---
EXOSCALE_API_KEY="EXOd4e0bc1d6ea62bf2d414b24e"
EXOSCALE_API_SECRET="ekOsjtNAEUCDD35rp2T80xQfqYQ4Bp1R1qxfjx1voKw"

# --- Script Start ---
echo "🚀 Starting Exoscale VPS setup..."

# 1. Install Exoscale CLI
if ! command -v exo &> /dev/null; then
    echo "🔧 Installing Exoscale CLI..."
    curl -fsSL https://raw.githubusercontent.com/exoscale/cli/master/install-latest.sh | sh
    # The script should add exo to the path, but we'll add it manually just in case
    export PATH=$PATH:/usr/local/bin/
    echo "✅ Exoscale CLI installed."
else
    echo "✅ Exoscale CLI already installed."
fi

# 2. Configure Exoscale CLI
echo "🔐 Configuring Exoscale CLI with your API keys..."
exo config -c default --key "$EXOSCALE_API_KEY" --secret "$EXOSCALE_API_SECRET"

# 3. Create SSH Key
if [ ! -f "~/.ssh/${SSH_KEY_NAME}" ]; then
    echo "🔑 Creating new SSH key: ${SSH_KEY_NAME}"
    ssh-keygen -t ed25519 -f "~/.ssh/${SSH_KEY_NAME}" -N ""
    exo compute ssh-key create "$SSH_KEY_NAME" -f "~/.ssh/${SSH_KEY_NAME}.pub"
    echo "✅ SSH key created and uploaded to Exoscale."
else
    echo "✅ SSH key already exists."
fi

# 4. Create Security Group with basic firewall rules
echo "🛡️  Creating security group: ${SECURITY_GROUP_NAME}"
exo compute security-group create "$SECURITY_GROUP_NAME" --description "Firewall for AI agent host"
exo compute security-group rule add "$SECURITY_GROUP_NAME" --protocol tcp --port 22 --cidr 0.0.0.0/0 --description "Allow SSH from anywhere"
exo compute security-group rule add "$SECURITY_GROUP_NAME" --protocol tcp --port 80 --cidr 0.0.0.0/0 --description "Allow HTTP from anywhere"
exo compute security-group rule add "$SECURITY_GROUP_NAME" --protocol tcp --port 443 --cidr 0.0.0.0/0 --description "Allow HTTPS from anywhere"
echo "✅ Security group created with SSH, HTTP, and HTTPS rules."

# 5. Create the Compute Instance
echo "💻 Creating compute instance: ${INSTANCE_NAME}..."
echo "   Type: ${INSTANCE_TYPE}, Zone: ${ZONE}, Disk: ${DISK_SIZE}GB"

# Cloud-init script to install Docker
cat << EOF > /tmp/cloud-init.yml
#cloud-config
packages:
  - docker.io
runcmd:
  - systemctl start docker
  - systemctl enable docker
  - usermod -aG docker ubuntu
EOF

exo compute instance create "$INSTANCE_NAME" \
    --zone "$ZONE" \
    --instance-type "$INSTANCE_TYPE" \
    --disk-size "$DISK_SIZE" \
    --template "$TEMPLATE_NAME" \
    --ssh-key "$SSH_KEY_NAME" \
    --security-group "$SECURITY_GROUP_NAME" \
    --cloud-init /tmp/cloud-init.yml

# 6. Get Instance IP and show SSH command
IP_ADDRESS=$(exo compute instance show "$INSTANCE_NAME" --output-template '{{.IPAddress}}')

echo "
🎉 Success! Your Exoscale VPS is ready.

IP Address: ${IP_ADDRESS}

To connect, use this command:
ssh -i ~/.ssh/${SSH_KEY_NAME} ubuntu@${IP_ADDRESS}

It may take a minute or two for the server to boot and install Docker.
"
