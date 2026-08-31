import streamlit as st

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pandas as pd


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="BASMA | AI Classroom Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# TIMEZONE
# =========================================================

BAHRAIN_TIMEZONE = ZoneInfo("Asia/Bahrain")


def get_bahrain_now():
    return datetime.now(BAHRAIN_TIMEZONE)


def get_bahrain_date():
    return get_bahrain_now().date()


# =========================================================
# IMPORT COMPONENTS
# =========================================================

from components.dashboard import (
    render_dashboard
)

from components.student_registration import (
    render_student_registration
)

from components.live_classroom import (
    render_live_classroom
)

from components.reports import (
    render_reports
)

from components.student_profile import (
    render_student_profile
)

from utils.data_manager import (
    load_students,
    load_attendance,
    load_activity
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* ================================
       MAIN
       ================================ */

    .main {
        background-color: #f8fafc;
    }

    /* ================================
       PAGE TITLE
       ================================ */

    .page-title {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .page-subtitle {
        color: #64748b;
        font-size: 16px;
        margin-bottom: 25px;
    }

    /* ================================
       SECTION LABEL
       ================================ */

    .section-label {
        font-size: 20px;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    /* ================================
       SIDEBAR
       ================================ */

    [data-testid="stSidebar"] {
        background-color: #f1f5f9;
    }

    /* ================================
       BUTTONS
       ================================ */

    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }

    /* ================================
       DOWNLOAD BUTTON
       ================================ */

    .stDownloadButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            text-align:center;
            padding:10px 0 20px 0;
        ">
            <h1 style="margin-bottom:0;">
                🌿 BASMA
            </h1>

            <p style="
                color:#64748b;
                margin-top:5px;
            ">
                AI Classroom Analytics
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Student Registration",
            "Live Classroom",
            "Student Profile",
            "Reports"
        ]
    )

    st.divider()

    # -------------------------------------
    # Bahrain date & time
    # -------------------------------------

    now = get_bahrain_now()

    st.caption(
        "🇧🇭 Bahrain Time"
    )

    st.write(
        now.strftime("%Y-%m-%d")
    )

    st.write(
        now.strftime("%H:%M:%S")
    )


# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.markdown(
        '<div class="page-title">Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">'
        'Classroom overview and student insights'
        '</div>',
        unsafe_allow_html=True
    )

    # -------------------------------------
    # Render Dashboard
    # -------------------------------------

    render_dashboard()

    # -------------------------------------
    # Load Data
    # -------------------------------------

    students = load_students()
    attendance = load_attendance()
    activities = load_activity()

    # =====================================
    # DOWNLOAD DASHBOARD DATA
    # =====================================

    st.markdown(
        '<div class="section-label">'
        'Download Dashboard Data'
        '</div>',
        unsafe_allow_html=True
    )

    download_col1, download_col2, download_col3 = st.columns(3)

    # -------------------------------------
    # Attendance CSV
    # -------------------------------------

    with download_col1:

        attendance_csv = (
            attendance
            .to_csv(index=False)
            .encode("utf-8")
        )

        st.download_button(
            label="📥 Download Attendance",
            data=attendance_csv,
            file_name="BASMA_Attendance.csv",
            mime="text/csv",
            use_container_width=True,
            key="dashboard_attendance_download"
        )

    # -------------------------------------
    # Activities CSV
    # -------------------------------------

    with download_col2:

        activities_csv = (
            activities
            .to_csv(index=False)
            .encode("utf-8")
        )

        st.download_button(
            label="📥 Download Activities",
            data=activities_csv,
            file_name="BASMA_Activities.csv",
            mime="text/csv",
            use_container_width=True,
            key="dashboard_activity_download"
        )

    # -------------------------------------
    # Students CSV
    # -------------------------------------

    with download_col3:

        students_csv = (
            students
            .to_csv(index=False)
            .encode("utf-8")
        )

        st.download_button(
            label="📥 Download Students",
            data=students_csv,
            file_name="BASMA_Students.csv",
            mime="text/csv",
            use_container_width=True,
            key="dashboard_students_download"
        )


# =========================================================
# STUDENT REGISTRATION
# =========================================================

elif page == "Student Registration":

    st.markdown(
        '<div class="page-title">'
        'Student Registration'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">'
        'Register students and create face embeddings'
        '</div>',
        unsafe_allow_html=True
    )

    render_student_registration()


# =========================================================
# LIVE CLASSROOM
# =========================================================

elif page == "Live Classroom":

    st.markdown(
        '<div class="page-title">'
        'Live Classroom'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">'
        'Monitor classroom activity using AI'
        '</div>',
        unsafe_allow_html=True
    )

    render_live_classroom()


# =========================================================
# STUDENT PROFILE
# =========================================================

elif page == "Student Profile":

    st.markdown(
        '<div class="page-title">'
        'Student Profile'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">'
        'View individual student performance'
        '</div>',
        unsafe_allow_html=True
    )

    render_student_profile()


# =========================================================
# REPORTS
# =========================================================

elif page == "Reports":

    st.markdown(
        '<div class="page-title">'
        'Reports'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">'
        'Attendance and classroom activity reports'
        '</div>',
        unsafe_allow_html=True
    )

    render_reports()
