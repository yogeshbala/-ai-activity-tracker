import smtplib
from email.mime.text import MIMEText
from db import check_today_log
from config import get_email_credentials

email_user, email_pass, recipient = get_email_credentials()

def send_reminder():
    if check_today_log(): return  # Already logged

    email_user, email_pass, recipient = get_email_credentials()
    msg = MIMEText("You haven't logged today's activities. Visit your dashboard.")
    msg['Subject'] = "⏰ Daily Log Reminder"
    msg['From'] = email_user
    msg['To'] = recipient

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(email_user, email_pass)
        server.send_message(msg)
