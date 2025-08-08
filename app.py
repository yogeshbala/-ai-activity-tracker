import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Initialize Firebase only once
if not firebase_admin._apps:
    firebase_config = {
        "type": st.secrets.FIREBASE.type,
        "project_id": st.secrets.FIREBASE.project_id,
        "private_key_id": st.secrets.FIREBASE.private_key_id,
        "private_key": st.secrets.FIREBASE.private_key.replace("\\n", "\n"),
        "client_email": st.secrets.FIREBASE.client_email,
        "client_id": st.secrets.FIREBASE.client_id,
        "auth_uri": st.secrets.FIREBASE.auth_uri,
        "token_uri": st.secrets.FIREBASE.token_uri,
        "auth_provider_x509_cert_url": st.secrets.FIREBASE.auth_provider_x509_cert_url,
        "client_x509_cert_url": st.secrets.FIREBASE.client_x509_cert_url,
        "universe_domain": st.secrets.FIREBASE.universe_domain
    }

    cred = credentials.Certificate(firebase_config)
    firebase_admin.initialize_app(cred)

# Connect to Firestore
db = firestore.client()

# Streamlit UI
st.set_page_config(page_title="Daily Input Tracker", page_icon="📝")
st.title("📝 Daily Input Tracker")

# Input form
user_input = st.text_area("Enter today's input")
today = datetime.now().strftime("%Y-%m-%d")

if st.button("Save Entry"):
    if user_input.strip():
        db.collection("daily_inputs").add({
            "input": user_input,
            "date": today,
            "timestamp": firestore.SERVER_TIMESTAMP
        })
        st.success("✅ Entry saved successfully!")
    else:
        st.warning("⚠️ Please enter something before saving.")

# Display previous entries
st.subheader("📜 Entry History")
docs = db.collection("daily_inputs").order_by("timestamp", direction=firestore.Query.DESCENDING).stream()

entries = []
st.subheader("📜 Entry History")
try:
    docs = db.collection("daily_inputs").order_by("date", direction=firestore.Query.DESCENDING).stream()
    entries = []
    for doc in docs:
        data = doc.to_dict()
        entries.append(f"📅 {data.get('date', 'Unknown')}: {data.get('input', '')}")

    if entries:
        for entry in entries:
            st.markdown(entry)
    else:
        st.info("No entries found yet.")
except Exception as e:
    st.error(f"⚠️ Failed to fetch entries: {e}")

if entries:
    for entry in entries:
        st.markdown(entry)
else:
    st.info("No entries found yet.")
