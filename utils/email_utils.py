import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import streamlit as st


# =========================================================
# SEND ATTENDANCE EMAIL
# =========================================================

def send_attendance_email(
    parent_email,
    student_name,
    time_str
):
    """
    Send an attendance notification email to the parent.

    Streamlit Secrets required:

        [email]
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "your_email@gmail.com"
        sender_password = "your_app_password"

    Returns:
        True  -> email sent successfully
        False -> email was not sent
    """

    # -----------------------------------------------------
    # Validate email
    # -----------------------------------------------------

    if not parent_email:

        return False

    parent_email = str(
        parent_email
    ).strip()

    if not parent_email:

        return False

    # -----------------------------------------------------
    # Load email settings
    # -----------------------------------------------------

    try:

        smtp_server = st.secrets["email"]["smtp_server"]

        smtp_port = int(
            st.secrets["email"]["smtp_port"]
        )

        sender_email = st.secrets["email"]["sender_email"]

        sender_password = st.secrets["email"]["sender_password"]

    except Exception as e:

        print(
            "Email secrets are not configured:",
            e
        )

        return False

    # -----------------------------------------------------
    # Email content
    # -----------------------------------------------------

    subject = (
        f"{student_name} has arrived at school"
    )

    body = (
        f"Dear Parent,\n\n"
        f"This is to let you know that "
        f"{student_name} was detected "
        f"in the classroom today at "
        f"{time_str}.\n\n"
        f"— BASMA AI Classroom Analytics"
    )

    message = MIMEMultipart()

    message["From"] = sender_email
    message["To"] = parent_email
    message["Subject"] = subject

    message.attach(
        MIMEText(
            body,
            "plain"
        )
    )

    # -----------------------------------------------------
    # Send email
    # -----------------------------------------------------

    try:

        with smtplib.SMTP(
            smtp_server,
            smtp_port,
            timeout=15
        ) as server:

            server.starttls()

            server.login(
                sender_email,
                sender_password
            )

            server.sendmail(
                sender_email,
                parent_email,
                message.as_string()
            )

        print(
            f"Email sent successfully to {parent_email}"
        )

        return True

    except Exception as e:

        print(
            f"Failed to send attendance email: {e}"
        )

        return False
