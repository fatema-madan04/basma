import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import pandas as pd
import streamlit as st


# =========================================================
# EMAIL SETTINGS
# =========================================================

def get_email_settings():

    try:

        settings = st.secrets["email"]

        smtp_server = str(
            settings["smtp_server"]
        )

        smtp_port = int(
            settings["smtp_port"]
        )

        sender_email = str(
            settings["sender_email"]
        )

        sender_password = str(
            settings["sender_password"]
        )

        return (
            smtp_server,
            smtp_port,
            sender_email,
            sender_password
        )

    except Exception as error:

        print(
            "Email settings error:",
            error
        )

        return None


# =========================================================
# SEND BASIC EMAIL
# =========================================================

def send_email(
    recipient,
    subject,
    body
):

    if not recipient:

        return False

    settings = get_email_settings()

    if settings is None:

        return False

    (
        smtp_server,
        smtp_port,
        sender_email,
        sender_password
    ) = settings

    message = MIMEMultipart()

    message["From"] = sender_email
    message["To"] = recipient
    message["Subject"] = subject

    message.attach(
        MIMEText(
            body,
            "plain"
        )
    )

    try:

        with smtplib.SMTP(
            smtp_server,
            smtp_port,
            timeout=20
        ) as server:

            server.starttls()

            server.login(
                sender_email,
                sender_password
            )

            server.sendmail(
                sender_email,
                recipient,
                message.as_string()
            )

        return True

    except Exception as error:

        print(
            "Email sending error:",
            error
        )

        return False


# =========================================================
# ATTENDANCE EMAIL
# =========================================================

def send_attendance_email(
    parent_email,
    student_name,
    time_str
):

    if not parent_email:

        return False

    subject = (
        f"{student_name} has arrived at school"
    )

    body = (
        "Dear Parent,\n\n"
        f"This is to let you know that "
        f"{student_name} was detected "
        f"in the classroom today at "
        f"{time_str}.\n\n"
        "— BASMA AI Classroom Analytics"
    )

    return send_email(
        recipient=parent_email,
        subject=subject,
        body=body
    )


# =========================================================
# BUILD ATTENDANCE REPORT
# =========================================================

def build_attendance_report(
    attendance,
    students,
    report_date=None
):

    if report_date is not None:

        attendance = attendance[
            attendance["date"].astype(str)
            == str(report_date)
        ].copy()

    if attendance.empty:

        return (
            "BASMA Attendance Report\n\n"
            "No attendance records found."
        )

    report = attendance.copy()

    # ---------------------------------------------
    # Add student names
    # ---------------------------------------------

    if not students.empty:

        student_names = students[
            [
                "student_id",
                "student_name"
            ]
        ].copy()

        student_names[
            "student_id"
        ] = student_names[
            "student_id"
        ].astype(str)

        report[
            "student_id"
        ] = report[
            "student_id"
        ].astype(str)

        report = report.merge(
            student_names,
            on="student_id",
            how="left"
        )

    else:

        report["student_name"] = (
            report["student_id"]
        )

    # ---------------------------------------------
    # Build text
    # ---------------------------------------------

    lines = [
        "BASMA AI Classroom Analytics",
        "Attendance Report",
        ""
    ]

    if report_date:

        lines.append(
            f"Date: {report_date}"
        )

        lines.append("")

    lines.append(
        f"Present Students: {len(report)}"
    )

    lines.append("")
    lines.append(
        "Student Attendance:"
    )

    lines.append(
        "--------------------------------"
    )

    for _, row in report.iterrows():

        name = str(
            row.get(
                "student_name",
                row["student_id"]
            )
        )

        first_seen = str(
            row.get(
                "first_seen",
                "-"
            )
        )

        last_seen = str(
            row.get(
                "last_seen",
                "-"
            )
        )

        lines.append(
            f"{name} | "
            f"First Seen: {first_seen} | "
            f"Last Seen: {last_seen}"
        )

    lines.append("")
    lines.append(
        "Generated by BASMA."
    )

    return "\n".join(lines)


# =========================================================
# SEND ATTENDANCE REPORT
# =========================================================

def send_attendance_report(
    recipient,
    attendance,
    students,
    report_date=None
):

    body = build_attendance_report(
        attendance=attendance,
        students=students,
        report_date=report_date
    )

    if report_date:

        subject = (
            f"BASMA Attendance Report — "
            f"{report_date}"
        )

    else:

        subject = (
            "BASMA Attendance Report"
        )

    return send_email(
        recipient=recipient,
        subject=subject,
        body=body
    )
