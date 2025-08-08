import streamlit as st

def get_openai_key():
    return st.secrets["OPENAI_API_KEY"]

def get_email_credentials():
    return (
        st.secrets["EMAIL_USER"],
        st.secrets["EMAIL_PASS"],
        st.secrets["EMAIL_USER"]  # recipient same as sender
    )
