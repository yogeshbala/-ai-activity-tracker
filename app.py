import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# --- Firebase Initialization ---
if not firebase_admin._apps:
    cred = credentials.Certificate(dict(st.secrets["firebase_credentials"]))
    firebase_admin.initialize_app(cred)

db = firestore.client()

st.title("🧠 Guided Daily Tracker")

# --- Morning Walk ---
walk_done = st.radio("🚶 Did you do your morning walk?", ["Yes", "No"])
walk_time = None
walk_reason = None
if walk_done == "Yes":
    walk_time = st.time_input("🕒 What time did you walk?")
else:
    walk_reason = st.text_area("❓ Why didn't you walk today?")

# --- Water Intake ---
water_litres = st.number_input("💧 How many litres of water did you drink today?", min_value=0.0, step=0.1)
if water_litres < 3.0:
    st.warning("⚠️ You haven't met your 3L goal today.")

# --- Sugar Consumption ---
sugar_taken = st.radio("🍬 Did you consume sugar today?", ["Yes", "No"])
sugar_reason = None
if sugar_taken == "Yes":
    sugar_reason = st.text_area("❓ What was the reason for consuming sugar?")

# --- Crypto Work ---
crypto_done = st.radio("📈 Did you complete your crypto-related work today?", ["Yes", "No"])

# --- Hair Care ---
hair_done = st.radio("🧴 Did you follow your hair care routine?", ["Yes", "No"])
hair_reason = None
if hair_done == "No":
    hair_reason = st.text_area("❓ Why didn't you do your hair care routine?")

# --- Unwanted Expense ---
expense_done = st.radio("💸 Did you make any unwanted expenses today?", ["Yes", "No"])

# --- Submit ---
if st.button("✅ Log Today's Activities"):
    doc = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "morning_walk": walk_done,
        "walk_time": str(walk_time) if walk_time else None,
        "walk_reason": walk_reason,
        "water_litres": water_litres,
        "sugar_taken": sugar_taken,
        "sugar_reason": sugar_reason,
        "crypto_done": crypto_done,
        "hair_done": hair_done,
        "hair_reason": hair_reason,
        "unwanted_expense": expense_done,
        "timestamp": firestore.SERVER_TIMESTAMP
    }
    db.collection("daily_logs").add(doc)
    st.success("🎉 Activities logged successfully!")
