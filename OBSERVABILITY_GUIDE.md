# Observability & Telemetry Guide
## Complete Monitoring Stack for Autonomous Agent System

**Status**: ✅ Operational
**Stack**: Prometheus + Grafana + cAdvisor + Node Exporter
**Last Updated**: October 22, 2025

---

## 📊 Overview

Your autonomous agent system now includes a production-grade observability stack that provides:
- **Real-time metrics** collection and visualization
- **Container-level monitoring** (CPU, memory, network, disk)
- **Host system monitoring** (system resources)
- **Custom agent metrics** (when instrumented)
- **Alerting rules** for proactive monitoring
- **Historical data** retention

---

## 🎯 Quick Access

### Monitoring Dashboards

| Service | URL | Credentials | Purpose |
|---------|-----|-------------|---------|
| **Grafana** | http://localhost:3000 | admin/admin | Main dashboards and visualization |
| **Prometheus** | http://localhost:9090 | None | Metrics database and query interface |
| **cAdvisor** | http://localhost:8082 | None | Container metrics UI |
| **Node Exporter** | http://localhost:9100/metrics | None | Host metrics (raw) |

**Note**: Change Grafana password on first login for production use.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│   Agents (agent-1 to agent-6)                     │
│   └─> Container Metrics (CPU, Memory, Network)    │
│                                                     │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │      cAdvisor        │
        │  (Container Metrics)  │
        └──────────┬───────────┘
                   │
        ┌──────────────────────┐
        │   Node Exporter      │
        │   (Host Metrics)     │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │    PROMETHEUS        │
        │  (Metrics Database)  │
        │  - Collects every 15s│
        │  - Stores time-series│
        │  - Evaluates alerts  │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │      GRAFANA         │
        │   (Visualization)    │
        │  - Custom dashboards │
        │  - Real-time graphs  │
        │  - Alert management  │
        └──────────────────────┘
```

---

## 📈 Metrics Being Collected

### 1. Container Metrics (via cAdvisor)

**Per-Container Metrics**:
- **CPU Usage**: `container_cpu_usage_seconds_total`
- **Memory Usage**: `container_memory_usage_bytes`
- **Memory Limit**: `container_spec_memory_limit_bytes`
- **Network I/O**: `container_network_receive_bytes_total`, `container_network_transmit_bytes_total`
- **Disk I/O**: `container_fs_reads_bytes_total`, `container_fs_writes_bytes_total`
- **Container Status**: `container_last_seen`

**Available for**: All 6 agents + monitoring containers

### 2. Host System Metrics (via Node Exporter)

**System-Level Metrics**:
- **CPU**: `node_cpu_seconds_total` (per core, per mode)
- **Memory**: `node_memory_MemTotal_bytes`, `node_memory_MemAvailable_bytes`
- **Disk**: `node_filesystem_size_bytes`, `node_filesystem_avail_bytes`
- **Network**: `node_network_receive_bytes_total`, `node_network_transmit_bytes_total`
- **Load Average**: `node_load1`, `node_load5`, `node_load15`
- **Uptime**: `node_boot_time_seconds`

### 3. Prometheus Self-Monitoring

- **Scrape Duration**: How long each metric collection takes
- **Scrape Success**: Whether metric collection succeeded
- **Time Series Count**: Number of metrics being tracked
- **Rule Evaluation**: Alert rule evaluation performance

---

## 🚀 Getting Started

### Step 1: Access Grafana

1. Open browser to **http://localhost:3000**
2. Login with:
   - Username: `admin`
   - Password: `admin`
3. Change password when prompted (recommended for production)

### Step 2: Verify Data Sources

1. Go to **Configuration** → **Data Sources**
2. You should see **Prometheus** configured and working
3. Click **Test** to verify connection

### Step 3: Create Your First Dashboard

#### Option A: Import Pre-built Dashboards

Grafana has excellent community dashboards. Import these IDs:

1. **Go to Dashboards** → **Import**
2. Enter dashboard ID and click **Load**:
   - **893** - Docker and System Monitoring
   - **14282** - cAdvisor Exporter
   - **1860** - Node Exporter Full
   - **11074** - Node Exporter for Prometheus

3. Select **Prometheus** as data source
4. Click **Import**

#### Option B: Create Custom Dashboard

1. **Dashboards** → **New Dashboard** → **Add Visualization**
2. Select **Prometheus** data source
3. Try these example queries:

**Agent CPU Usage**:
```promql
rate(container_cpu_usage_seconds_total{name=~"agent-.*"}[5m]) * 100
```

**Agent Memory Usage (MB)**:
```promql
container_memory_usage_bytes{name=~"agent-.*"} / 1024 / 1024
```

**Agent Count (should be 6)**:
```promql
count(container_last_seen{name=~"agent-.*"})
```

**System CPU Usage**:
```promql
100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```

**System Memory Usage %**:
```promql
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100
```

---

## 📊 Recommended Dashboards

### Dashboard 1: Agent Overview

**Panels to create**:
1. **Agent Status** (Stat panel)
   - Query: `count(up{job="agents"} == 1)`
   - Shows: Number of healthy agents

2. **Total CPU Usage** (Gauge)
   - Query: `sum(rate(container_cpu_usage_seconds_total{name=~"agent-.*"}[5m])) * 100`
   - Threshold: 0-50 (green), 50-80 (yellow), 80-100 (red)

3. **Total Memory Usage** (Gauge)
   - Query: `sum(container_memory_usage_bytes{name=~"agent-.*"}) / 1024 / 1024 / 1024`
   - Unit: GB

4. **CPU per Agent** (Time series)
   - Query: `rate(container_cpu_usage_seconds_total{name=~"agent-.*"}[5m]) * 100`
   - Legend: `{{name}}`

5. **Memory per Agent** (Time series)
   - Query: `container_memory_usage_bytes{name=~"agent-.*"} / 1024 / 1024`
   - Legend: `{{name}}`
   - Unit: MB

6. **Network I/O** (Time series)
   - RX: `rate(container_network_receive_bytes_total{name=~"agent-.*"}[5m])`
   - TX: `rate(container_network_transmit_bytes_total{name=~"agent-.*"}[5m])`

### Dashboard 2: System Health

**Panels**:
1. **System CPU %** (Time series + Gauge)
2. **System Memory %** (Time series + Gauge)
3. **Disk Usage %** (Gauge per mount point)
4. **Network Throughput** (Time series)
5. **Load Average** (Time series - 1m, 5m, 15m)
6. **Uptime** (Stat)

### Dashboard 3: Agent Performance (Advanced)

When agents are instrumented with custom metrics:
- Task completion rate
- API call duration
- Error rate
- Cost per task
- Queue depth

---

## 🚨 Alerting

### Current Alert Rules

Located in: `/monitoring/prometheus/alerts.yml`

**Critical Alerts**:
1. **AgentDown**: Agent container stopped (triggers after 2 minutes)
2. **HostHighCPU**: System CPU > 90% for 5 minutes
3. **HostHighMemory**: System memory > 90% for 5 minutes

**Warning Alerts**:
1. **HighCPUUsage**: Container CPU > 80% for 5 minutes
2. **HighMemoryUsage**: Container memory > 85% for 5 minutes
3. **HostHighDisk**: Disk usage > 85%

### View Active Alerts

**In Prometheus**:
1. Go to http://localhost:9090/alerts
2. See all alert rules and their current status

**In Grafana**:
1. Go to **Alerting** → **Alert Rules**
2. Configure notification channels (Slack, email, etc.)

### Configure Alert Notifications

1. **Grafana** → **Alerting** → **Contact Points**
2. **Add Contact Point**
3. Choose notification method:
   - Email
   - Slack
   - PagerDuty
   - Webhook
   - Discord
4. Test and Save

---

## 🔍 Querying Metrics

### Prometheus Query Language (PromQL)

Access the query interface at http://localhost:9090/graph

**Example Queries**:

```promql
# Show all agent containers
up{job="agents"}

# Total memory used by all agents (in MB)
sum(container_memory_usage_bytes{name=~"agent-.*"}) / 1024 / 1024

# Agent with highest CPU usage
topk(1, rate(container_cpu_usage_seconds_total{name=~"agent-.*"}[5m]))

# Memory usage percentage per agent
(container_memory_usage_bytes{name=~"agent-.*"} /
 container_spec_memory_limit_bytes{name=~"agent-.*"}) * 100

# Network bandwidth per agent (last minute)
sum by (name) (
  rate(container_network_receive_bytes_total{name=~"agent-.*"}[1m]) +
  rate(container_network_transmit_bytes_total{name=~"agent-.*"}[1m])
)

# Agents that restarted in last hour
changes(container_start_time_seconds{name=~"agent-.*"}[1h]) > 0
```

### Useful PromQL Functions

- `rate()` - Per-second rate over time range
- `increase()` - Total increase over time range
- `sum()` - Add values together
- `avg()` - Average values
- `max()` / `min()` - Maximum/minimum values
- `topk()` / `bottomk()` - Top/bottom K values
- `count()` - Count number of time series

---

## 🛠️ Configuration

### Prometheus Configuration

**File**: `monitoring/prometheus/prometheus.yml`

**Scrape Intervals**:
- Global: 15 seconds (good balance of detail vs. storage)
- Evaluation: 15 seconds (alert check frequency)

**To add new metrics target**:
```yaml
scrape_configs:
  - job_name: 'my-service'
    static_configs:
      - targets: ['my-service:9090']
        labels:
          service: 'my-service'
```

**Reload configuration** (without restart):
```bash
curl -X POST http://localhost:9090/-/reload
```

### Grafana Configuration

**Persistent Data**: Stored in Docker volume `exoscale_deployment_grafana-data`

**Change Admin Password**:
1. Login to Grafana
2. Profile (bottom left) → **Change Password**

**Add Users**:
1. **Configuration** → **Users** → **Invite**
2. Choose role: Viewer, Editor, or Admin

### Data Retention

**Prometheus** (default):
- Retention: 15 days
- Storage: `/prometheus` in container
- Volume: `exoscale_deployment_prometheus-data`

**To change retention**:
Edit `docker-compose.yml`:
```yaml
prometheus:
  command:
    - '--storage.tsdb.retention.time=30d'  # 30 days
    - '--storage.tsdb.retention.size=10GB'  # or size limit
```

---

## 📱 Mobile Access

### Grafana Mobile App

1. Download **Grafana Mobile** (iOS/Android)
2. Add server: http://your-server-ip:3000
3. Login with your credentials
4. View dashboards on-the-go

### Web Mobile

Just visit http://your-server-ip:3000 on mobile browser - Grafana is fully responsive.

---

## 🔧 Troubleshooting

### Monitoring Stack Issues

**Check monitoring services status**:
```bash
docker-compose ps | grep -E "(prometheus|grafana|cadvisor|node-exporter)"
```

**View monitoring logs**:
```bash
docker-compose logs -f prometheus
docker-compose logs -f grafana
docker-compose logs -f cadvisor
```

**Restart monitoring stack**:
```bash
docker-compose restart prometheus grafana cadvisor node-exporter
```

### Common Issues

**1. Grafana shows "No Data"**
- Check Prometheus is running: `curl http://localhost:9090/-/healthy`
- Verify data source in Grafana: Configuration → Data Sources → Test
- Check Prometheus targets: http://localhost:9090/targets (should all be "UP")

**2. Prometheus not scraping metrics**
- Check target status: http://localhost:9090/targets
- If target is "DOWN", check container is running
- Verify network connectivity between containers

**3. cAdvisor not showing metrics**
- Check cAdvisor is accessible: http://localhost:8082
- Verify Docker socket is mounted: `docker inspect cadvisor | grep docker.sock`
- Check cAdvisor logs: `docker-compose logs cadvisor`

**4. Alerts not firing**
- Check alert rules: http://localhost:9090/alerts
- Verify alert rules syntax: `docker-compose exec prometheus promtool check rules /etc/prometheus/alerts.yml`
- Check Grafana notification channels are configured

**5. High disk usage**
- Check Prometheus data size: `docker-compose exec prometheus du -sh /prometheus`
- Reduce retention time in docker-compose.yml
- Clear old data: `docker-compose restart prometheus`

### Reset Monitoring Data

**Clear Prometheus data**:
```bash
docker-compose stop prometheus
docker volume rm exoscale_deployment_prometheus-data
docker-compose up -d prometheus
```

**Reset Grafana** (loses dashboards and users):
```bash
docker-compose stop grafana
docker volume rm exoscale_deployment_grafana-data
docker-compose up -d grafana
```

---

## 🚀 Advanced Features

### Service Discovery

For dynamic environments, configure Prometheus service discovery:

```yaml
scrape_configs:
  - job_name: 'docker'
    docker_sd_configs:
      - host: unix:///var/run/docker.sock
    relabel_configs:
      - source_labels: [__meta_docker_container_name]
        target_label: container
```

### Recording Rules

Precompute expensive queries for faster dashboards:

**File**: `monitoring/prometheus/recording_rules.yml`
```yaml
groups:
  - name: agent_recording_rules
    interval: 30s
    rules:
      - record: agent:cpu_usage:rate5m
        expr: rate(container_cpu_usage_seconds_total{name=~"agent-.*"}[5m])

      - record: agent:memory_usage_percent
        expr: (container_memory_usage_bytes{name=~"agent-.*"} /
               container_spec_memory_limit_bytes{name=~"agent-.*"}) * 100
```

Add to prometheus.yml:
```yaml
rule_files:
  - 'recording_rules.yml'
```

### Grafana Provisioning

Auto-create dashboards on startup by adding JSON files to:
`monitoring/grafana/provisioning/dashboards/`

---

## 📊 Resource Usage

**Monitoring Stack Overhead**:
- **Prometheus**: 0.5 CPU, 512MB RAM (~50MB disk per day)
- **Grafana**: 0.5 CPU, 512MB RAM (~100MB disk total)
- **cAdvisor**: 0.3 CPU, 256MB RAM (minimal disk)
- **Node Exporter**: 0.2 CPU, 128MB RAM (no disk)

**Total**: ~1.5 CPU cores, 1.4GB RAM

---

## 📝 Best Practices

### Dashboard Design

1. **Start simple** - Create basic dashboards first, add complexity later
2. **Group related metrics** - CPU, memory, network together
3. **Use consistent time ranges** - Default to last 1 hour or 6 hours
4. **Add descriptions** - Panel descriptions help others understand metrics
5. **Set appropriate thresholds** - Green/yellow/red zones for gauges

### Alert Configuration

1. **Avoid alert fatigue** - Only alert on actionable items
2. **Use appropriate thresholds** - Not too sensitive, not too lenient
3. **Add runbooks** - Include resolution steps in alert annotations
4. **Test alerts** - Trigger test alerts to verify notifications work
5. **Group related alerts** - Reduce notification spam

### Query Optimization

1. **Use recording rules** - For frequently used complex queries
2. **Limit time ranges** - Don't query years of data unnecessarily
3. **Use appropriate intervals** - `[5m]` for most queries is sufficient
4. **Aggregate when possible** - Use `sum()`, `avg()` to reduce series

---

## 🎯 Next Steps

### Immediate Actions

1. **Access Grafana**: http://localhost:3000 (admin/admin)
2. **Import community dashboards**: IDs 893, 14282, 1860
3. **Verify metrics**: Check Prometheus targets are "UP"
4. **Create first custom dashboard**: Agent CPU & Memory overview

### This Week

1. **Instrument agents** with custom metrics endpoints
2. **Set up alert notifications** (Slack, email)
3. **Create business metrics** dashboard (tasks, costs, ROI)
4. **Configure dashboard** auto-refresh (30s or 1m)

### This Month

1. **Long-term metrics** analysis and trending
2. **Capacity planning** based on growth patterns
3. **SLO/SLA** dashboards for uptime and performance
4. **Cost tracking** dashboard (API usage, infrastructure)

---

## 📚 Additional Resources

**Prometheus**:
- Docs: https://prometheus.io/docs/
- Query examples: https://prometheus.io/docs/prometheus/latest/querying/examples/
- Best practices: https://prometheus.io/docs/practices/naming/

**Grafana**:
- Docs: https://grafana.com/docs/grafana/latest/
- Dashboard gallery: https://grafana.com/grafana/dashboards/
- Tutorials: https://grafana.com/tutorials/

**PromQL**:
- Cheat sheet: https://promlabs.com/promql-cheat-sheet/
- Query builder: http://localhost:9090/graph

---

## 🏁 Summary

You now have a **complete observability and telemetry stack** monitoring your autonomous agent system!

**What's Monitored**:
- ✅ All 6 agent containers (CPU, memory, network, disk)
- ✅ Host system resources
- ✅ Container health and restarts
- ✅ Real-time metrics with 15-second granularity
- ✅ Alert rules for critical issues
- ✅ 15 days of historical data

**Access Points**:
- **Grafana**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090
- **cAdvisor**: http://localhost:8082

**Next**: Create your first dashboard and start visualizing your agent performance!

---

**Version**: 1.0.0
**Status**: ✅ Operational
**Last Updated**: October 22, 2025
