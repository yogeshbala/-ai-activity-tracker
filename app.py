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

# --- Sidebar Navigation ---
st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio("Go to", ["Daily Tracker", "Dashboard"])

# --- Page 1: Daily Tracker ---
if page == "Daily Tracker":
    st.title("🧠 Guided Daily Tracker")

    # Morning Walk
    walk_done = st.radio("🚶 Did you do your morning walk?", ["Yes", "No"])
    walk_time = None
    walk_reason = None
    if walk_done == "Yes":
        walk_time = st.time_input("🕒 What time did you walk?")
    else:
        walk_reason = st.text_area("❓ Why didn't you walk today?")

    # Water Intake
    water_litres = st.number_input("💧 How many litres of water did you drink today?", min_value=0.0, step=0.1)
    if water_litres < 3.0:
        st.warning("⚠️ You haven't met your 3L goal today.")

    # Sugar Consumption
    sugar_taken = st.radio("🍬 Did you consume sugar today?", ["Yes", "No"])
    sugar_reason = None
    if sugar_taken == "Yes":
        sugar_reason = st.text_area("❓ What was the reason for consuming sugar?")

    # Crypto Work
    crypto_done = st.radio("📈 Did you complete your crypto-related work today?", ["Yes", "No"])

    # Hair Care
    hair_done = st.radio("🧴 Did you follow your hair care routine?", ["Yes", "No"])
    hair_reason = None
    if hair_done == "No":
        hair_reason = st.text_area("❓ Why didn't you do your hair care routine?")

    # Unwanted Expense
    expense_done = st.radio("💸 Did you make any unwanted expenses today?", ["Yes", "No"])

    # Submit
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

# --- Page 2: Dashboard ---
elif page == "Dashboard":
    st.title("📊 Daily Tracker Dashboard")

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
        # Morning Walk
        st.subheader("🚶 Morning Walk")
        walk_df = df[["date", "morning_walk", "walk_time", "walk_reason"]]
        st.dataframe(walk_df)
        st.line_chart(walk_df.set_index("date")["morning_walk"].apply(lambda x: 1 if x == "Yes" else 0))

        # Water Intake
        st.subheader("💧 Water Intake")
        st.line_chart(df.set_index("date")["water_litres"])
        below_goal = df[df["water_litres"] < 3.0]
        st.write(f"🔻 Days below 3L goal: {len(below_goal)}")

        # Sugar Consumption
        st.subheader("🍬 Sugar Consumption")
        sugar_df = df[["date", "sugar_taken", "sugar_reason"]]
        st.dataframe(sugar_df)
        st.bar_chart(sugar_df.set_index("date")["sugar_taken"].apply(lambda x: 1 if x == "Yes" else 0))

        # Crypto Work
        st.subheader("📈 Crypto Work")
        st.line_chart(df.set_index("date")["crypto_done"].apply(lambda x: 1 if x == "Yes" else 0))

        # Hair Care
        st.subheader("🧴 Hair Care Routine")
        hair_df = df[["date", "hair_done", "hair_reason"]]
        st.dataframe(hair_df)
        st.line_chart(hair_df.set_index("date")["hair_done"].apply(lambda x: 1 if x == "Yes" else 0))

        # Unwanted Expenses
        st.subheader("💸 Unwanted Expenses")
        st.line_chart(df.set_index("date")["unwanted_expense"].apply(lambda x: 1 if x == "Yes" else 0))
