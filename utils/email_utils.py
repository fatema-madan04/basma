import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import streamlit as st


# =========================================================
# EMAIL SETTINGS
# =========================================================

def get_email_settings():

    try:

        email_settings = st.secrets["email"]

        smtp_server = str(
            email_settings["smtp_server"]
        ).strip()

        smtp_port = int(
            email_settings["smtp_port"]
        )

        sender_email = str(
            email_settings["sender_email"]
        ).strip()

        sender_password = str(
            email_settings["sender_password"]
        ).strip()

        return (
            smtp_server,
            smtp_port,
            sender_email,
            sender_password
        )

    except Exception as e:

        raise RuntimeError(
            f"Email settings are missing or incorrect: {e}"
        )


# =========================================================
# SEND ATTENDANCE EMAIL
# =========================================================

def send_attendance_email(
    parent_email,
    student_name,
    time_str
):

    # -----------------------------------------------------
    # Validate Parent Email
    # -----------------------------------------------------

    if parent_email is None:

        return False

    parent_email = str(
        parent_email
    ).strip()

    if not parent_email:

        return False


    # -----------------------------------------------------
    # Get Email Settings
    # -----------------------------------------------------

    try:

        (
            smtp_server,
            smtp_port,
            sender_email,
            sender_password
        ) = get_email_settings()

    except Exception as e:

        st.error(
            f"❌ Email configuration error: {e}"
        )

        return False


    # -----------------------------------------------------
    # Email Content
    # -----------------------------------------------------

    subject = (
        f"BASMA Attendance Alert — {student_name}"
    )

    body = (
        f"Dear Parent,\n\n"

        f"This is to inform you that "
        f"{student_name} has been detected "
        f"in the classroom today.\n\n"

        f"Attendance Time: {time_str}\n"

        f"Status: Present\n\n"

        f"Best regards,\n"
        f"BASMA AI Classroom Analytics"
    )


    # -----------------------------------------------------
    # Create Email
    # -----------------------------------------------------

    message = MIMEMultipart()

    message["From"] = sender_email

    message["To"] = parent_email

    message["Subject"] = subject

    message.attach(
        MIMEText(
            body,
            "plain",
            "utf-8"
        )
    )


    # -----------------------------------------------------
    # Send Email
    # -----------------------------------------------------

    try:

        with smtplib.SMTP(
            smtp_server,
            smtp_port,
            timeout=20
        ) as server:

            server.ehlo()

            server.starttls()

            server.ehlo()

            server.login(
                sender_email,
                sender_password
            )

            server.sendmail(
                sender_email,
                [parent_email],
                message.as_string()
            )


        print(
            f"Attendance email sent successfully "
            f"to {parent_email}"
        )

        return True


    except smtplib.SMTPAuthenticationError:

        st.error(
            "❌ Gmail authentication failed. "
            "Check the sender email and App Password."
        )

        return False


    except smtplib.SMTPRecipientsRefused:

        st.error(
            f"❌ Gmail rejected the parent email: "
            f"{parent_email}"
        )

        return False


    except smtplib.SMTPConnectError:

        st.error(
            "❌ Could not connect to the email server."
        )

        return False


    except Exception as e:

        st.error(
            f"❌ Email sending failed: {e}"
        )

        return False
