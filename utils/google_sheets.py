import streamlit as st
import pandas as pd


# =========================================================
# GOOGLE SHEETS
# =========================================================

def get_google_client():

    try:

        import gspread

        credentials = dict(
            st.secrets[
                "google_service_account"
            ]
        )

        client = (
            gspread
            .service_account_from_dict(
                credentials
            )
        )

        return client

    except Exception as error:

        print(
            "Google Sheets connection error:",
            error
        )

        return None


# =========================================================
# GET SPREADSHEET
# =========================================================

def get_spreadsheet():

    client = get_google_client()

    if client is None:

        return None

    try:

        spreadsheet_name = str(
            st.secrets[
                "google_sheets"
            ]["spreadsheet_name"]
        )

        spreadsheet = client.open(
            spreadsheet_name
        )

        return spreadsheet

    except Exception as error:

        print(
            "Google Spreadsheet error:",
            error
        )

        return None


# =========================================================
# WRITE DATAFRAME TO SHEET
# =========================================================

def write_dataframe(
    spreadsheet,
    sheet_name,
    dataframe
):

    try:

        try:

            worksheet = (
                spreadsheet
                .worksheet(sheet_name)
            )

        except Exception:

            worksheet = (
                spreadsheet
                .add_worksheet(
                    title=sheet_name,
                    rows=1000,
                    cols=20
                )
            )

        dataframe = dataframe.copy()

        dataframe = dataframe.fillna("")

        values = [
            dataframe.columns.tolist()
        ]

        values += (
            dataframe.astype(str)
            .values
            .tolist()
        )

        worksheet.clear()

        worksheet.update(
            range_name="A1",
            values=values
        )

        return True

    except Exception as error:

        print(
            f"Google Sheets write error "
            f"({sheet_name}):",
            error
        )

        return False


# =========================================================
# SYNC ATTENDANCE
# =========================================================

def sync_attendance(
    attendance
):

    spreadsheet = get_spreadsheet()

    if spreadsheet is None:

        return False

    return write_dataframe(
        spreadsheet=spreadsheet,
        sheet_name="Attendance",
        dataframe=attendance
    )


# =========================================================
# SYNC ACTIVITIES
# =========================================================

def sync_activities(
    activities
):

    spreadsheet = get_spreadsheet()

    if spreadsheet is None:

        return False

    return write_dataframe(
        spreadsheet=spreadsheet,
        sheet_name="Activities",
        dataframe=activities
    )


# =========================================================
# SYNC ALL DATA
# =========================================================

def sync_all_data(
    attendance,
    activities
):

    spreadsheet = get_spreadsheet()

    if spreadsheet is None:

        return False

    attendance_result = write_dataframe(
        spreadsheet=spreadsheet,
        sheet_name="Attendance",
        dataframe=attendance
    )

    activity_result = write_dataframe(
        spreadsheet=spreadsheet,
        sheet_name="Activities",
        dataframe=activities
    )

    return (
        attendance_result
        and activity_result
    )

