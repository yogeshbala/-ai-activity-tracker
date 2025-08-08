import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Load credentials from st.secrets
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
db = firestore.client()

# Input form
st.title("Daily Input Tracker")
user_input = st.text_input("Enter today's input")

if st.button("Save"):
    db.collection("daily_inputs").add({
        "input": user_input,
        "date": str(st.session_state.get("date", "2025-08-09"))
    })
    st.success("Input saved!")

# Display history
st.subheader("Previous Entries")
docs = db.collection("daily_inputs").stream()
for doc in docs:
    st.write(doc.to_dict())
