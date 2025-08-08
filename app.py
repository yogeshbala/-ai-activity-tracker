import streamlit as st
from datetime import date
from activities import get_tasks
from metrics import calculate_metrics
from ai_feedback import generate_suggestions
from db import save_log, load_today_log

st.set_page_config(page_title="Daily Activity Tracker", layout="centered")
st.title("🧠 Daily Activity Tracker")

today = str(date.today())
tasks = get_tasks()
log = load_today_log(today)
completed = []
skipped = {}

st.subheader(f"Tasks for {today}")
for task in tasks:
    status = st.radio(f"{task}", ["Not completed", "Completed"], key=task)
    if status == "Completed":
        completed.append(task)
    else:
        reason = st.text_input(f"Why did you skip '{task}'?", key=f"{task}_reason")
        skipped[task] = reason

if st.button("Submit"):
    save_log(today, completed, skipped)
    st.success("✅ Activities logged!")

    completion_rate, streak = calculate_metrics()
    st.metric("Completion Rate", f"{completion_rate}%")
    st.metric("Streak", f"{streak} days")

    if skipped:
        st.subheader("💡 Suggestions")
        for task, reason in skipped.items():
            suggestion = generate_suggestions(task, reason)
            st.write(f"- {task}: {suggestion}")
