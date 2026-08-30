import json

import gspread
import streamlit as st

from google.oauth2.service_account import Credentials


# =========================================================
# GOOGLE SHEETS SETTINGS
# =========================================================

SHEET_ID = st.secrets["GOOGLE_SHEET_ID"]

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


# =========================================================
# CONNECT TO GOOGLE SHEETS
# =========================================================

def get_google_sheet():

    service_account_data = json.loads(
        st.secrets["GOOGLE_SERVICE_ACCOUNT"]
    )

    credentials = Credentials.from_service_account_info(
        service_account_data,
        scopes=SCOPES
    )

    client = gspread.authorize(
        credentials
    )

    spreadsheet = client.open_by_key(
        SHEET_ID
    )

    return spreadsheet


# =========================================================
# GET / CREATE WORKSHEET
# =========================================================

def get_or_create_worksheet(
    spreadsheet,
    worksheet_name,
    headers
):

    try:

        worksheet = spreadsheet.worksheet(
            worksheet_name
        )

    except gspread.WorksheetNotFound:

        worksheet = spreadsheet.add_worksheet(
            title=worksheet_name,
            rows=1000,
            cols=len(headers)
        )

        worksheet.append_row(
            headers
        )

    # Add headers if sheet exists but is empty
    if not worksheet.get_all_values():

        worksheet.append_row(
            headers
        )

    return worksheet


# =========================================================
# ATTENDANCE
# =========================================================

def sync_attendance(
    student_id,
    date,
    first_seen,
    last_seen,
    status
):

    try:

        spreadsheet = get_google_sheet()

        worksheet = get_or_create_worksheet(
            spreadsheet,
            "Attendance",
            [
                "Student ID",
                "Date",
                "First Seen",
                "Last Seen",
                "Status"
            ]
        )

        records = worksheet.get_all_records()

        # ---------------------------------------------
        # Check if attendance already exists
        # ---------------------------------------------

        existing_row = None

        for index, record in enumerate(
            records,
            start=2
        ):

            if (
                str(record.get("Student ID", ""))
                == str(student_id)
                and str(record.get("Date", ""))
                == str(date)
            ):

                existing_row = index
                break

        # ---------------------------------------------
        # Update existing attendance
        # ---------------------------------------------

        if existing_row:

            worksheet.update(
                range_name=f"A{existing_row}:E{existing_row}",
                values=[[
                    student_id,
                    date,
                    first_seen,
                    last_seen,
                    status
                ]]
            )

        # ---------------------------------------------
        # Add new attendance
        # ---------------------------------------------

        else:

            worksheet.append_row([
                student_id,
                date,
                first_seen,
                last_seen,
                status
            ])

        return True

    except Exception as error:

        print(
            f"Google Sheets attendance sync failed: {error}"
        )

        return False


# =========================================================
# ACTIVITY
# =========================================================

def sync_activity(
    student_id,
    date,
    time,
    activity
):

    try:

        spreadsheet = get_google_sheet()

        worksheet = get_or_create_worksheet(
            spreadsheet,
            "Activities",
            [
                "Student ID",
                "Date",
                "Time",
                "Activity"
            ]
        )

        worksheet.append_row([
            student_id,
            date,
            time,
            activity
        ])

        return True

    except Exception as error:

        print(
            f"Google Sheets activity sync failed: {error}"
        )

        return False

