import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
from datetime import datetime

# --- Firebase Initialization ---
if not firebase_admin._apps:
    cred = credentials.Certificate(dict(st.secrets["firebase_credentials"]))
    firebase_admin.initialize_app(cred)

db = firestore.client()

st.title("📊 Daily Tracker Dashboard")

# --- Fetch Data ---
docs = db.collection("daily_logs").order_by("date").stream()
data = []
for doc in docs:
    entry = doc.to_dict()
    entry["date"] = pd.to_datetime(entry["date"])
    data.append(entry)

df = pd.DataFrame(data).sort_values("date")

if df.empty:
    st.info("No data logged yet.")
else:
    # --- Morning Walk ---
    st.subheader("🚶 Morning Walk")
    walk_df = df[["date", "morning_walk", "walk_time", "walk_reason"]]
    st.dataframe(walk_df)
    st.line_chart(walk_df.set_index("date")["morning_walk"].apply(lambda x: 1 if x == "Yes" else 0))

    # --- Water Intake ---
    st.subheader("💧 Water Intake")
    st.line_chart(df.set_index("date")["water_litres"])
    below_goal = df[df["water_litres"] < 3.0]
    st.write(f"🔻 Days below 3L goal: {len(below_goal)}")

    # --- Sugar Consumption ---
    st.subheader("🍬 Sugar Consumption")
    sugar_df = df[["date", "sugar_taken", "sugar_reason"]]
    st.dataframe(sugar_df)
    st.bar_chart(sugar_df.set_index("date")["sugar_taken"].apply(lambda x: 1 if x == "Yes" else 0))

    # --- Crypto Work ---
    st.subheader("📈 Crypto Work")
    st.line_chart(df.set_index("date")["crypto_done"].apply(lambda x: 1 if x == "Yes" else 0))

    # --- Hair Care Routine ---
    st.subheader("🧴 Hair Care Routine")
    hair_df = df[["date", "hair_done", "hair_reason"]]
    st.dataframe(hair_df)
    st.line_chart(hair_df.set_index("date")["hair_done"].apply(lambda x: 1 if x == "Yes" else 0))

    # --- Unwanted Expenses ---
    st.subheader("💸 Unwanted Expenses")
    st.line_chart(df.set_index("date")["unwanted_expense"].apply(lambda x: 1 if x == "Yes" else 0))
