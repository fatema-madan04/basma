from pathlib import Path
from datetime import datetime

import pandas as pd

from utils.google_sheets import (
    sync_attendance,
    sync_activity
)


# =========================================================
# DATA FILES
# =========================================================

DATA_FOLDER = Path("data")

STUDENTS_FILE = DATA_FOLDER / "students.csv"
ATTENDANCE_FILE = DATA_FOLDER / "attendance.csv"
ACTIVITY_FILE = DATA_FOLDER / "activity_log.csv"
TEACHER_NOTES_FILE = DATA_FOLDER / "teacher_notes.csv"


# Make sure the data folder exists
DATA_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# STUDENTS
# =========================================================

def load_students():

    if not STUDENTS_FILE.exists():

        return pd.DataFrame(
            columns=[
                "student_id",
                "student_name",
                "parent_email",
                "parent_phone",
                "photo_path"
            ]
        )

    try:

        # IMPORTANT: force student_id to be read as text.
        # Without this, pandas auto-detects numeric-looking IDs
        # (e.g. "01") and converts them to integers (1), losing
        # the leading zero. The face-recognition side keeps the
        # original string ID, so the two stop matching and the
        # app falls back to showing the raw ID instead of the
        # student's name.
        students = pd.read_csv(
            STUDENTS_FILE,
            dtype={"student_id": str}
        )

    except pd.errors.EmptyDataError:

        return pd.DataFrame(
            columns=[
                "student_id",
                "student_name",
                "parent_email",
                "parent_phone",
                "photo_path"
            ]
        )

    return students


def save_student(
    student_id,
    student_name,
    parent_email,
    parent_phone,
    photo_path
):

    students = load_students()

    new_student = {
        "student_id": student_id,
        "student_name": student_name,
        "parent_email": parent_email,
        "parent_phone": parent_phone,
        "photo_path": photo_path
    }

    students.loc[
        len(students)
    ] = new_student

    students.to_csv(
        STUDENTS_FILE,
        index=False
    )


# =========================================================
# ATTENDANCE
# =========================================================

def load_attendance():

    if not ATTENDANCE_FILE.exists():

        return pd.DataFrame(
            columns=[
                "student_id",
                "date",
                "first_seen",
                "last_seen",
                "status"
            ]
        )

    try:

        # Same leading-zero fix as load_students().
        attendance = pd.read_csv(
            ATTENDANCE_FILE,
            dtype={"student_id": str, "date": str}
        )

    except pd.errors.EmptyDataError:

        return pd.DataFrame(
            columns=[
                "student_id",
                "date",
                "first_seen",
                "last_seen",
                "status"
            ]
        )

    return attendance


def save_attendance(
    student_id,
    date,
    time
):
    """
    Save or update attendance.

    Returns:
        True  -> first attendance record today
        False -> student already recorded today
    """

    attendance = load_attendance()

    # -----------------------------------------------------
    # Check if student already has attendance today
    # -----------------------------------------------------

    already_marked = (
        (attendance["student_id"].astype(str) == str(student_id))
        & (attendance["date"].astype(str) == str(date))
    ).any()

    # =====================================================
    # STUDENT ALREADY RECORDED TODAY
    # =====================================================

    if already_marked:

        mask = (
            (attendance["student_id"].astype(str) == str(student_id))
            & (attendance["date"].astype(str) == str(date))
        )

        # Update Last Seen
        attendance.loc[
            mask,
            "last_seen"
        ] = time

        # Save local CSV
        attendance.to_csv(
            ATTENDANCE_FILE,
            index=False
        )

        # Get current attendance record
        row = attendance.loc[
            mask
        ].iloc[0]

        # Update Google Sheets
        sync_attendance(
            student_id=student_id,
            date=date,
            first_seen=row["first_seen"],
            last_seen=time,
            status=row["status"]
        )

        return False

    # =====================================================
    # FIRST ATTENDANCE TODAY
    # =====================================================

    new_record = {
        "student_id": student_id,
        "date": date,
        "first_seen": time,
        "last_seen": time,
        "status": "Present"
    }

    attendance.loc[
        len(attendance)
    ] = new_record

    # Save local CSV
    attendance.to_csv(
        ATTENDANCE_FILE,
        index=False
    )

    # Add to Google Sheets
    sync_attendance(
        student_id=student_id,
        date=date,
        first_seen=time,
        last_seen=time,
        status="Present"
    )

    return True


# =========================================================
# ACTIVITY
# =========================================================

def load_activity():

    if not ACTIVITY_FILE.exists():

        return pd.DataFrame(
            columns=[
                "student_id",
                "date",
                "time",
                "activity"
            ]
        )

    try:

        # Same leading-zero fix as load_students().
        activity = pd.read_csv(
            ACTIVITY_FILE,
            dtype={"student_id": str, "date": str}
        )

    except pd.errors.EmptyDataError:

        return pd.DataFrame(
            columns=[
                "student_id",
                "date",
                "time",
                "activity"
            ]
        )

    return activity


def save_activity(
    student_id,
    date,
    time,
    activity
):

    activities = load_activity()

    new_activity = {
        "student_id": student_id,
        "date": date,
        "time": time,
        "activity": activity
    }

    activities.loc[
        len(activities)
    ] = new_activity

    # Save local CSV
    activities.to_csv(
        ACTIVITY_FILE,
        index=False
    )

    # Add to Google Sheets
    sync_activity(
        student_id=student_id,
        date=date,
        time=time,
        activity=activity
    )


# =========================================================
# TEACHER NOTES
# =========================================================

def load_teacher_notes():

    if not TEACHER_NOTES_FILE.exists():

        return pd.DataFrame(
            columns=[
                "student_id",
                "date",
                "time",
                "note"
            ]
        )

    try:

        notes = pd.read_csv(
            TEACHER_NOTES_FILE
        )

    except pd.errors.EmptyDataError:

        return pd.DataFrame(
            columns=[
                "student_id",
                "date",
                "time",
                "note"
            ]
        )

    return notes


def save_teacher_note(
    student_id,
    note
):

    notes = load_teacher_notes()

    now = datetime.now()

    new_note = {
        "student_id": student_id,
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "note": note
    }

    notes.loc[
        len(notes)
    ] = new_note

    notes.to_csv(
        TEACHER_NOTES_FILE,
        index=False
    )
