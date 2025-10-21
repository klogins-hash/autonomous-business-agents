# Deployment Guide: Exoscale Multi-Agent System

This guide provides a step-by-step walkthrough to deploy your multi-agent system on an Exoscale VPS. This setup is designed for AI agents that can edit their own code, with full SSH access for you to supervise and manage the system.

## Prerequisites

1.  **Your Exoscale API Keys**: You have already provided these.
2.  **A local terminal**: You can use the Terminal app on your Mac or any Linux terminal.

---

## Part 1: Setting Up Your Local Machine

This part only needs to be done once.

### Step 1: Open Your Terminal

*   **On Mac**: Open `Terminal.app` from your Applications/Utilities folder.
*   **On Linux**: Open your preferred terminal application.

### Step 2: Run the VPS Setup Script

This script will create your Exoscale VPS. It's designed to be run from your local machine.

1.  **Navigate to the `exoscale_deployment` directory** you received.

2.  **Make the script executable**:
    ```bash
    chmod +x setup_vps.sh
    ```

3.  **Run the script**:
    ```bash
    ./setup_vps.sh
    ```

4.  **Follow the prompts**: The script will guide you through installing the Exoscale CLI, configuring your API keys, and creating the VPS. It will automatically handle SSH key generation and security group setup.

5.  **Save the SSH Command**: At the end, the script will output the IP address of your new server and the exact SSH command to connect to it. **Save this command!** It will look like this:
    ```bash
    ssh -i ~/.ssh/agent-vps-key ubuntu@<YOUR_SERVER_IP>
    ```

---

## Part 2: Deploying Your Agents

Now that your VPS is running, you can deploy your agents.

### Step 1: Connect to Your VPS

1.  Open your local terminal.
2.  Use the SSH command you saved from Part 1 to connect to your server.

### Step 2: Upload the Deployment Files

1.  From your local machine's terminal (not the SSH session), use `scp` (Secure Copy) to upload the entire `exoscale_deployment` directory to your new server. Replace `<YOUR_SERVER_IP>` with your server's IP address.

    ```bash
    scp -r -i ~/.ssh/agent-vps-key ./exoscale_deployment ubuntu@<YOUR_SERVER_IP>:~/ 
    ```
    This command recursively copies the folder to your home directory on the VPS.

### Step 3: Start the Agents

1.  If you're not already, SSH into your VPS.

2.  **Navigate to the deployment directory**:
    ```bash
    cd ~/exoscale_deployment
    ```

3.  **Build and run the agent containers** using Docker Compose:
    ```bash
    docker-compose up -d --build
    ```
    *   `up` starts the services.
    *   `-d` runs them in the background (detached mode).
    *   `--build` tells Docker Compose to build the agent image from the Dockerfile before starting.

Your agents are now running on the VPS!

---

## Part 3: Managing Your Agents

With everything running, here are the common commands you'll use to manage your agents via SSH.

### View Agent Logs

To see the real-time output of all your agents:
```bash
docker-compose logs -f
```

To view logs for a specific agent (e.g., `agent-1`):
```bash
docker-compose logs -f agent-1
```

### Stop and Start Agents

*   **Stop all agents**:
    ```bash
    docker-compose stop
    ```
*   **Start all agents**:
    ```bash
    docker-compose start
    ```
*   **Restart all agents**:
    ```bash
    docker-compose restart
    ```

### Access an Agent's Container

If you need to get a shell inside a running agent's container for debugging:
```bash
docker exec -it agent-1 bash
```
This gives you a bash shell inside the `agent-1` container. You can look around, check files, and see the agent's environment from its own perspective.

### Edit Agent Code

Because the agent code directories are mounted as volumes, you can edit the code directly on the VPS, and the changes will be reflected inside the containers.

1.  **SSH into your VPS**.
2.  **Navigate to the agent's code directory**, for example:
    ```bash
    cd ~/exoscale_deployment/agent-1-code
    ```
3.  **Edit the files** using a terminal editor like `nano` or `vim`:
    ```bash
    nano agent.py
    ```
4.  **Restart the agent** for the changes to take effect (if your agent doesn't automatically detect them):
    ```bash
    docker-compose restart agent-1
    ```

---

## Part 4: Moving to Autonomous Operation

When you're confident in an agent's behavior and want it to run fully autonomously:

1.  **SSH into your VPS**.
2.  **Edit the `docker-compose.yml` file**:
    ```bash
    nano ~/exoscale_deployment/docker-compose.yml
    ```
3.  **Find the agent service** you want to make autonomous (e.g., `agent-1`).
4.  **Change the `APPROVAL_REQUIRED` environment variable** from `true` to `false`.
5.  **Save the file** and exit the editor.
6.  **Re-deploy the agent** with the new configuration:
    ```bash
    docker-compose up -d --build agent-1
    ```

The agent will now operate autonomously, modifying its own code as programmed.

