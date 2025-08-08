import os
import streamlit as st

def get_openai_key():
    return st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")

def get_email_credentials():
    if "EMAIL_USER" in st.secrets:
        return st.secrets["EMAIL_USER"], st.secrets["EMAIL_PASS"], st.secrets["EMAIL_USER"]
    return os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"), os.getenv("EMAIL_USER")
