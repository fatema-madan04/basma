from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

import streamlit as st

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
# Dashboard Settings
# =========================================

if "dashboard_settings" not in st.session_state:

    st.session_state.dashboard_settings = {
        "show_metrics": True,
        "show_activity": True,
        "show_attendance": True,
        "show_profile": True,
        "show_performance": True
    }


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

    # -------------------------------------
    # Bahrain Time
    # -------------------------------------

    bahrain_time = datetime.now(
        ZoneInfo("Asia/Bahrain")
    )

    current_hour = bahrain_time.hour

    if current_hour < 12:

        greeting = "Good Morning"

    elif current_hour < 18:

        greeting = "Good Afternoon"

    else:

        greeting = "Good Evening"

    # -------------------------------------
    # Header
    # -------------------------------------

    st.markdown(
        f'<div class="page-title">'
        f'{greeting}, Teacher 👋'
        f'</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">'
        "Here's today's classroom overview."
        '</div>',
        unsafe_allow_html=True
    )

    # -------------------------------------
    # Load Data
    # -------------------------------------

    students = load_students()
    activities = load_activity()

    # -------------------------------------
    # Dashboard Filters
    # -------------------------------------

    st.markdown(
        '<div class="dashboard-filter-box">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="filter-title">'
        'Dashboard Filters'
        '</div>',
        unsafe_allow_html=True
    )

    filter_col1, filter_col2 = st.columns(2)

    # -------------------------------------
    # Student Filter
    # -------------------------------------

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
            student_options,
            key="dashboard_student"
        )

    # -------------------------------------
    # Activity Filter
    # -------------------------------------

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
            activity_options,
            key="dashboard_activity"
        )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    # =====================================
    # METRIC CARDS
    # =====================================

    if st.session_state.dashboard_settings[
        "show_metrics"
    ]:

        st.markdown(
            '<div class="section-label">'
            'Classroom Overview'
            '</div>',
            unsafe_allow_html=True
        )

        render_metric_cards()

    # =====================================
    # ACTIVITY + ATTENDANCE
    # =====================================

    show_activity = (
        st.session_state.dashboard_settings[
            "show_activity"
        ]
    )

    show_attendance = (
        st.session_state.dashboard_settings[
            "show_attendance"
        ]
    )

    # -------------------------------------
    # Both enabled
    # -------------------------------------

    if show_activity and show_attendance:

        chart_col, attendance_col = st.columns(
            [2.2, 1]
        )

        with chart_col:

            # IMPORTANT:
            # Current charts.py does not accept
            # an activity parameter.

            render_class_activity_chart()

        with attendance_col:

            render_attendance_chart()

    # -------------------------------------
    # Activity only
    # -------------------------------------

    elif show_activity:

        render_class_activity_chart()

    # -------------------------------------
    # Attendance only
    # -------------------------------------

    elif show_attendance:

        render_attendance_chart()

    # =====================================
    # STUDENT PROFILE + PERFORMANCE
    # =====================================

    show_profile = (
        st.session_state.dashboard_settings[
            "show_profile"
        ]
    )

    show_performance = (
        st.session_state.dashboard_settings[
            "show_performance"
        ]
    )

    # -------------------------------------
    # Find selected student ID
    # -------------------------------------

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

    # -------------------------------------
    # Both enabled
    # -------------------------------------

    if show_profile and show_performance:

        profile_col, performance_col = st.columns(
            [1.15, 1]
        )

        with profile_col:

            render_student_profile()

        with performance_col:

            render_performance_chart(
                selected_student_id
            )

    # -------------------------------------
    # Profile only
    # -------------------------------------

    elif show_profile:

        render_student_profile()

    # -------------------------------------
    # Performance only
    # -------------------------------------

    elif show_performance:

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

    # =====================================
    # Dashboard Customization
    # =====================================

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
        "Choose which sections you want "
        "to display on your dashboard."
    )

    settings = (
        st.session_state.dashboard_settings
    )

    settings["show_metrics"] = st.checkbox(
        "Show Metric Cards",
        value=settings["show_metrics"],
        key="setting_metrics"
    )

    settings["show_activity"] = st.checkbox(
        "Show Class Activity",
        value=settings["show_activity"],
        key="setting_activity"
    )

    settings["show_attendance"] = st.checkbox(
        "Show Attendance",
        value=settings["show_attendance"],
        key="setting_attendance"
    )

    settings["show_profile"] = st.checkbox(
        "Show Student Profile",
        value=settings["show_profile"],
        key="setting_profile"
    )

    settings["show_performance"] = st.checkbox(
        "Show Student Performance",
        value=settings["show_performance"],
        key="setting_performance"
    )

    st.session_state.dashboard_settings = settings

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    # =====================================
    # System Information
    # =====================================

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

    st.write(
        "Timezone: Bahrain (UTC+3)"
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )
