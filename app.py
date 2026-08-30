from pathlib import Path

import streamlit as st
import pandas as pd

from components.live_classroom import (
    render_live_classroom
)

from components.sidebar import (
    render_sidebar
)

from components.student_registration import (
    render_student_registration
)

from components.cards import (
    render_metric_cards
)

from components.charts import (
    render_class_activity_chart,
    render_attendance_chart,
    render_performance_chart
)

from components.student_profile import (
    render_student_profile
)

from utils.data_manager import (
    load_students,
    load_activity
)


# =========================================
# Page Configuration
# =========================================

st.set_page_config(
    page_title="BASMA — AI Classroom Analytics",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================
# Load Theme
# =========================================

theme_path = Path(
    "styles/basma_theme.css"
)

if theme_path.exists():

    with open(
        theme_path,
        "r",
        encoding="utf-8"
    ) as file:

        css = file.read()

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True
    )


# =========================================
# Sidebar
# =========================================

selected_page = render_sidebar()


# =========================================
# Student Registration
# =========================================

if selected_page == "📝 Student Registration":

    render_student_registration()


# =========================================
# Dashboard
# =========================================

elif selected_page == "🏠 Dashboard":

    st.markdown(
        '<div class="page-title">'
        'Good Morning, Teacher 👋'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">'
        "Here's today's classroom overview."
        '</div>',
        unsafe_allow_html=True
    )

    # =====================================
    # DASHBOARD FILTERS
    # =====================================

    st.markdown(
        '<div class="filter-title">'
        'Dashboard Filters'
        '</div>',
        unsafe_allow_html=True
    )

    students = load_students()
    activities = load_activity()

    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:

        student_options = [
            "All Students"
        ]

        if not students.empty:

            student_options += (
                students[
                    "student_name"
                ]
                .dropna()
                .astype(str)
                .tolist()
            )

        selected_student = st.selectbox(
            "Student",
            student_options
        )

    with filter_col2:

        activity_options = [
            "All Activities"
        ]

        if not activities.empty:

            activity_options += (
                activities[
                    "activity"
                ]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

        selected_activity = st.selectbox(
            "Activity",
            activity_options
        )

    # =====================================
    # KPI CARDS
    # =====================================

    st.markdown(
        '<div class="section-label">'
        'Classroom Overview'
        '</div>',
        unsafe_allow_html=True
    )

    render_metric_cards()

    # =====================================
    # MAIN CHARTS
    # =====================================

    chart_col, attendance_col = st.columns(
        [2.2, 1]
    )

    with chart_col:

        render_class_activity_chart(
            selected_activity
        )

    with attendance_col:

        render_attendance_chart()

    # =====================================
    # STUDENT SECTION
    # =====================================

    profile_col, performance_col = st.columns(
        [1.15, 1]
    )

    with profile_col:

        render_student_profile()

    with performance_col:

        selected_student_id = None

        if (
            selected_student != "All Students"
            and not students.empty
        ):

            selected_rows = students[
                students["student_name"]
                == selected_student
            ]

            if not selected_rows.empty:

                selected_student_id = (
                    selected_rows.iloc[0][
                        "student_id"
                    ]
                )

        render_performance_chart(
            selected_student_id
        )


# =========================================
# Live Classroom
# =========================================

elif selected_page == "📹 Live Classroom":

    render_live_classroom()


# =========================================
# Student Profile
# =========================================

elif selected_page == "👤 Student Profile":

    render_student_profile()


# =========================================
# Analytics
# =========================================

elif selected_page == "📊 Analytics":

    st.markdown(
        '<div class="page-title">'
        'Analytics'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">'
        'Analyze classroom attendance and '
        'student activities.'
        '</div>',
        unsafe_allow_html=True
    )

    render_class_activity_chart()

    col1, col2 = st.columns(2)

    with col1:

        render_attendance_chart()

    with col2:

        render_performance_chart()


# =========================================
# Settings
# =========================================

elif selected_page == "⚙️ Settings":

    st.markdown(
        '<div class="page-title">'
        'Settings'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">'
        'Customize your BASMA dashboard.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="settings-card">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="panel-title">'
        'Dashboard Customization'
        '</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Choose which dashboard sections "
        "you want to display."
    )

    show_metrics = st.checkbox(
        "Show Metric Cards",
        value=True
    )

    show_activity = st.checkbox(
        "Show Class Activity",
        value=True
    )

    show_attendance = st.checkbox(
        "Show Attendance",
        value=True
    )

    show_profile = st.checkbox(
        "Show Student Profile",
        value=True
    )

    show_performance = st.checkbox(
        "Show Student Performance",
        value=True
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="panel">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="panel-title">'
        'System Information'
        '</div>',
        unsafe_allow_html=True
    )

    st.write(
        "BASMA AI Classroom Analytics"
    )

    st.write(
        "YOLO classroom activity detection "
        "is enabled."
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )
