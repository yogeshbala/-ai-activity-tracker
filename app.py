import streamlit as st
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase (use your secrets config)
cred = credentials.Certificate(st.secrets["firebase_credentials"])
firebase_admin.initialize_app(cred)
db = firestore.client()

# Daily log form
st.title("🗓️ Daily Activity Tracker")

with st.form("daily_log"):
    walk_time = st.time_input("🕒 Morning Walk Time", value=datetime.now().time())
    whey_taken = st.checkbox("💪 Whey Protein Taken")
    water_intake = st.number_input("💧 Litres of Water Consumed", min_value=0.0, step=0.1)
    sugar_free = st.checkbox("🚫 No Sugar Consumed")
    crypto_work = st.text_input("🧠 Crypto Work Done")
    hair_care = st.checkbox("🧴 Hair Care Done")
    no_expense = st.checkbox("💸 No Unwanted Expense Today")

    submitted = st.form_submit_button("Log Activities")
    if submitted:
        log_data = {
            "timestamp": datetime.now(),
            "walk_time": str(walk_time),
            "whey_taken": whey_taken,
            "water_intake": water_intake,
            "sugar_free": sugar_free,
            "crypto_work": crypto_work,
            "hair_care": hair_care,
            "no_expense": no_expense
        }
        db.collection("daily_logs").add(log_data)
        st.success("✅ Activities logged successfully!")
