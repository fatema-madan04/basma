import streamlit as st
import pandas as pd
import plotly.express as px

from datetime import datetime
from zoneinfo import ZoneInfo

from utils.data_manager import (
    load_students,
    load_attendance,
    load_activity
)


# =========================================================
# TIMEZONE
# =========================================================

BAHRAIN_TIMEZONE = ZoneInfo(
    "Asia/Bahrain"
)


# =========================================================
# ACTIVITY CLASSES
# =========================================================

ACTIVITY_CLASSES = [
    "Clapping",
    "Facing-Forward",
    "Hand-Raising",
    "Reading",
    "Sleeping",
    "Talking",
    "Using-Phone",
    "Writing"
]


# =========================================================
# CLASS ACTIVITY CHART
# =========================================================

def render_class_activity_chart():

    activities = load_activity()

    st.markdown(
        "### 🎯 Class Activity"
    )

    if activities.empty:

        st.info(
            "No classroom activity data available."
        )

        return

    # -------------------------------------
    # Count activities
    # -------------------------------------

    activity_counts = (
        activities["activity"]
        .astype(str)
        .value_counts()
        .reset_index()
    )

    activity_counts.columns = [
        "Activity",
        "Count"
    ]

    # -------------------------------------
    # Chart
    # -------------------------------------

    fig = px.bar(
        activity_counts,
        x="Activity",
        y="Count",
        title="Classroom Activity Detection",
        text="Count"
    )

    fig.update_layout(
        height=400,
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),
        xaxis_title="Activity",
        yaxis_title="Detections"
    )

    fig.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# ATTENDANCE CHART
# =========================================================

def render_attendance_chart():

    attendance = load_attendance()

    st.markdown(
        "### 👥 Attendance"
    )

    if attendance.empty:

        st.info(
            "No attendance data available."
        )

        return

    # -------------------------------------
    # Bahrain Today
    # -------------------------------------

    today = datetime.now(
        BAHRAIN_TIMEZONE
    ).strftime(
        "%Y-%m-%d"
    )

    # -------------------------------------
    # Make sure date is string
    # -------------------------------------

    attendance["date"] = (
        attendance["date"]
        .astype(str)
    )

    # -------------------------------------
    # Today's attendance
    # -------------------------------------

    today_attendance = attendance[
        attendance["date"] == today
    ]

    # -------------------------------------
    # No records today
    # -------------------------------------

    if today_attendance.empty:

        st.info(
            "No attendance recorded today."
        )

        return

    # -------------------------------------
    # Present count
    # -------------------------------------

    present_count = len(
        today_attendance
    )

    # -------------------------------------
    # Display metric
    # -------------------------------------

    st.metric(
        "Present Today",
        present_count
    )

    # -------------------------------------
    # Attendance chart
    # -------------------------------------

    chart_data = pd.DataFrame(
        {
            "Status": [
                "Present"
            ],
            "Students": [
                present_count
            ]
        }
    )

    fig = px.pie(
        chart_data,
        names="Status",
        values="Students",
        title="Today's Attendance"
    )

    fig.update_layout(
        height=350,
        margin=dict(
            l=10,
            r=10,
            t=60,
            b=10
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# PERFORMANCE CHART
# =========================================================

def render_performance_chart(
    selected_student_id=None
):

    attendance = load_attendance()

    activities = load_activity()

    students = load_students()

    st.markdown(
        "### 📈 Student Performance"
    )

    # -------------------------------------
    # No students
    # -------------------------------------

    if students.empty:

        st.info(
            "No students registered yet."
        )

        return

    # -------------------------------------
    # Filter student
    # -------------------------------------

    if selected_student_id is not None:

        student_id = str(
            selected_student_id
        )

        attendance = attendance[
            attendance[
                "student_id"
            ].astype(str)
            == student_id
        ]

        activities = activities[
            activities[
                "student_id"
            ].astype(str)
            == student_id
        ]

    # -------------------------------------
    # Attendance count
    # -------------------------------------

    attendance_count = len(
        attendance
    )

    # -------------------------------------
    # Activity count
    # -------------------------------------

    activity_count = len(
        activities
    )

    # -------------------------------------
    # Performance data
    # -------------------------------------

    performance_data = pd.DataFrame(
        {
            "Metric": [
                "Attendance",
                "Activities"
            ],
            "Count": [
                attendance_count,
                activity_count
            ]
        }
    )

    # -------------------------------------
    # Chart
    # -------------------------------------

    fig = px.bar(
        performance_data,
        x="Metric",
        y="Count",
        text="Count",
        title="Student Performance Overview"
    )

    fig.update_layout(
        height=350,
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),
        xaxis_title="",
        yaxis_title="Count"
    )

    fig.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
