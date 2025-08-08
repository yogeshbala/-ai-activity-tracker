import json
import os

LOG_FILE = "activity_logs.json"

def load_all_logs():
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r") as f:
        return json.load(f)

def load_today_log(date):
    logs = load_all_logs()
    for log in logs:
        if log["date"] == date:
            return log
    return {"date": date, "tasks": [], "completed": [], "skipped": {}}

def save_log(date, completed, skipped):
    logs = load_all_logs()
    tasks = completed + list(skipped.keys())
    new_log = {
        "date": date,
        "tasks": tasks,
        "completed": completed,
        "skipped": skipped
    }
    logs = [log for log in logs if log["date"] != date]
    logs.append(new_log)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

def check_today_log():
    from datetime import date
    today = str(date.today())
    log = load_today_log(today)
    return bool(log["completed"] or log["skipped"])
