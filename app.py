import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# --- Firebase Initialization ---
if not firebase_admin._apps:
    cred = credentials.Certificate(dict(st.secrets["firebase_credentials"]))
    firebase_admin.initialize_app(cred)

db = firestore.client()

# --- Streamlit UI ---
st.title("🗓️ Daily Activity Tracker")

# Activity Inputs
morning_walk = st.time_input("🚶 Morning Walk Time", value=datetime.strptime("00:00", "%H:%M").time())
whey_taken = st.checkbox("💪 Whey Protein Taken")
water_litres = st.number_input("💧 Litres of Water Consumed", min_value=0.0, step=0.1)
no_sugar = st.checkbox("🚫 No Sugar Consumed")
crypto_work = st.checkbox("📈 Crypto Work Done")
hair_care = st.checkbox("🧴 Hair Care Done")
no_expense = st.checkbox("💸 No Unwanted Expense Today")

# --- Check for No Activity ---
no_activity = (
    morning_walk == datetime.strptime("00:00", "%H:%M").time() and
    not whey_taken and
    water_litres == 0.0 and
    not no_sugar and
    not crypto_work and
    not hair_care and
    not no_expense
)

# --- Reason Prompt ---
if no_activity:
    reason = st.text_area(
        "⚠️ No activities logged today. Would you like to share why?",
        placeholder="e.g., rest day, travel, not feeling well..."
    )
else:
    reason = None

# --- Submit Button ---
if st.button("✅ Log Today's Activities"):
    doc = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "morning_walk": str(morning_walk),
        "whey_taken": whey_taken,
        "water_litres": water_litres,
        "no_sugar": no_sugar,
        "crypto_work": crypto_work,
        "hair_care": hair_care,
        "no_expense": no_expense,
        "reason": reason,
        "timestamp": firestore.SERVER_TIMESTAMP
    }
    db.collection("daily_logs").add(doc)
    st.success("🎉 Activities logged successfully!")
