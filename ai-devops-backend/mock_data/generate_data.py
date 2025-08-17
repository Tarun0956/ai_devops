import json
import random
from datetime import datetime, timedelta

# --- Generate Logs ---
log_levels = ["INFO", "WARN", "ERROR", "DEBUG"]
components = ["Auth", "DB", "API", "Worker", "Scheduler"]
logs = []

for i in range(1, 21):
    logs.append({
        "timestamp": (datetime.now() - timedelta(minutes=i*10)).isoformat(),
        "log_level": random.choice(log_levels),
        "component": random.choice(components),
        "message": random.choice([
            "Operation completed successfully",
            "Connection failed",
            "Timeout occurred",
            "Task scheduled",
            "Memory usage high",
            "Dependency missing"
        ])
    })

# --- Generate Tasks ---
statuses = ["To Do", "In Progress", "Done", "Blocked"]
priorities = ["Low", "Medium", "High","Critical"]
users = ["Alice", "Bob", "Charlie", "David","Eve"]

tasks = []
for i in range(1, 11):
    created_at = datetime.now() - timedelta(days=random.randint(0, 10))
    completed_at = created_at + timedelta(days=random.randint(0, 5)) if random.random() > 0.3 else None
    tasks.append({
        "task_id": f"TASK-{i}",
        "jira_ticket": f"JIRA-{1000+i}",
        "status": random.choice(statuses),
        "assigned_to": random.choice(users),
        "priority": random.choice(priorities),
        "created_at": created_at.isoformat(),
        "completed_at": completed_at.isoformat() if completed_at else None
    })

# --- Generate Metrics ---
metrics = []
for i in range(1, 51):
    metrics.append({
        "timestamp": (datetime.now() - timedelta(minutes=i*5)).isoformat(),
        "cpu_usage": random.randint(30, 95),
        "memory_usage": random.randint(40, 90),
        "disk_io": random.randint(100, 1000),
        "network_latency": random.randint(1, 200)
    })

# --- Save JSON files ---
import os
os.makedirs("./mock_data", exist_ok=True)

with open("./mock_data/logs.json", "w") as f:
    json.dump(logs, f, indent=4)

with open("./mock_data/tasks.json", "w") as f:
    json.dump(tasks, f, indent=4)

with open("./mock_data/metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)

print("Synthetic data generated successfully!")
