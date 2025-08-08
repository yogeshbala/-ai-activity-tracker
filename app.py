import streamlit as st
from datetime import date
import os
from dotenv import load_dotenv

load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

st.title("🧠 Daily Activity Tracker")
tasks = ["Code 2 hours", "Workout", "Read 30 mins"]
today = str(date.today())
completed = []
skipped = {}

st.subheader(f"Tasks for {today}")
for task in tasks:
    status = st.radio(f"{task}", ["Not completed", "Completed"])
    if status == "Completed":
        completed.append(task)
    else:
        reason = st.text_input(f"Why did you skip '{task}'?", key=task)
        skipped[task] = reason

if st.button("Submit"):
    st.success("Activities logged!")
    # Save to DB or file here
