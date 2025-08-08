
from db import load_all_logs

def calculate_metrics():
    logs = load_all_logs()
    total_tasks = 0
    completed_tasks = 0
    streak = 0

    for log in logs[::-1]:  # reverse chronological
        total_tasks += len(log["tasks"])
        completed_tasks += len(log["completed"])
        if len(log["completed"]) == len(log["tasks"]):
            streak += 1
        else:
            break

    completion_rate = int((completed_tasks / total_tasks) * 100) if total_tasks else 0
    return completion_rate, streak
