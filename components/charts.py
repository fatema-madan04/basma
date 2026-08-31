import streamlit as st
import pandas as pd
import plotly.express as px


from utils.data_manager import (
    load_students,
    load_attendance,
    load_activity
)


# =========================================================
# FIXED ACTIVITY CLASSES
# =========================================================
# These are the exact 8 class names basma_yolo.pt was trained
# on (checked directly against the model's own model.names).
# Used so the Activity filter and the Class Activity chart
# always list all 8 classes, even ones with zero detections
# so far — not just whatever happens to already be in
# activity_log.csv.

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
# ATTENDANCE CHART
# =========================================================

def render_attendance_chart(
    attendance_date=None
):

    students = load_students()
    attendance = load_attendance()

    total_students = len(
        students
    )

    if total_students == 0:

        st.info(
            "No students registered yet."
        )

        return

    # -----------------------------------------------------
    # Date
    # -----------------------------------------------------

    if attendance_date is None:

        attendance_date = (
            pd.Timestamp.now()
            .strftime("%Y-%m-%d")
        )

    # -----------------------------------------------------
    # Filter attendance by date
    # -----------------------------------------------------

    today_attendance = attendance[
        attendance["date"].astype(str)
        == str(attendance_date)
    ]

    # -----------------------------------------------------
    # Present students
    # -----------------------------------------------------

    present = today_attendance[
        today_attendance["status"] == "Present"
    ]["student_id"].astype(str).nunique()

    # -----------------------------------------------------
    # Absent students
    # -----------------------------------------------------

    absent = max(
        total_students - present,
        0
    )

    # -----------------------------------------------------
    # Chart data
    # -----------------------------------------------------

    data = pd.DataFrame({
        "Status": [
            "Present",
            "Absent"
        ],
        "Students": [
            present,
            absent
        ]
    })

    # -----------------------------------------------------
    # Panel
    # -----------------------------------------------------

    st.markdown(
        '<div class="panel">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="panel-title">'
        'Today\'s Attendance'
        '</div>',
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # Attendance rate
    # -----------------------------------------------------

    attendance_rate = (
        (present / total_students) * 100
        if total_students > 0
        else 0
    )

    # -----------------------------------------------------
    # Pie chart
    # -----------------------------------------------------

    chart = px.pie(
        data,
        values="Students",
        names="Status",
        hole=0.72,
        color="Status",
        color_discrete_map={
            "Present": "#8BC59C",
            "Absent": "#E8E6C7"
        }
    )

    chart.update_layout(
        height=260,
        margin=dict(
            l=0,
            r=0,
            t=0,
            b=0
        ),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        annotations=[
            dict(
                text=(
                    f"<b>{present}</b><br>"
                    "<span style='font-size:10px'>"
                    "Present"
                    "</span>"
                ),
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(
                    size=18,
                    color="#527B68"
                )
            )
        ]
    )

    st.plotly_chart(
        chart,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )

    # -----------------------------------------------------
    # Summary
    # -----------------------------------------------------

    st.markdown(
        f"🟢 Present: **{present}** &nbsp;&nbsp;"
        f"🟡 Absent: **{absent}**"
    )

    st.caption(
        f"Attendance Rate: "
        f"{attendance_rate:.1f}%"
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# CLASS ACTIVITY CHART
# =========================================================

def render_class_activity_chart(
    selected_activity="All Activities"
):

    activities = load_activity()

    # -----------------------------------------------------
    # Clean activity values (safe even if the log is empty —
    # we still want to draw all 8 classes at zero below)
    # -----------------------------------------------------

    activities = activities.copy()

    if "activity" not in activities.columns:

        activities["activity"] = pd.Series(dtype=str)

    activities["activity"] = (
        activities["activity"]
        .astype(str)
        .str.strip()
    )

    # -----------------------------------------------------
    # Count activities — always show all 8 fixed classes
    # (zero-filled), not just the ones detected so far.
    # -----------------------------------------------------

    if (
        selected_activity
        and selected_activity != "All Activities"
    ):

        filtered = activities[
            activities["activity"]
            == str(selected_activity)
        ]

        activity_counts = pd.DataFrame({
            "Activity": [selected_activity],
            "Count": [len(filtered)]
        })

    else:

        counts = (
            activities["activity"]
            .value_counts()
            .reindex(ACTIVITY_CLASSES, fill_value=0)
        )

        activity_counts = (
            counts
            .rename_axis("Activity")
            .reset_index(name="Count")
        )

    # -----------------------------------------------------
    # Panel
    # -----------------------------------------------------

    st.markdown(
        '<div class="panel">',
        unsafe_allow_html=True
    )

    if (
        selected_activity
        and selected_activity != "All Activities"
    ):

        title = (
            f"Class Activity — "
            f"{selected_activity}"
        )

    else:

        title = "Class Activity"

    st.markdown(
        f'<div class="panel-title">'
        f'{title}'
        f'</div>',
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # Bar chart
    # -----------------------------------------------------

    chart = px.bar(
        activity_counts,
        x="Activity",
        y="Count",
        text="Count"
    )

    # Match the app's sage-green theme instead of Plotly's
    # default blue.
    chart.update_traces(
        marker_color="#6F9E87"
    )

    chart.update_layout(
        height=320,
        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Manrope",
            size=10,
            color="#8A948D"
        ),
        xaxis=dict(
            title="",
            showgrid=False
        ),
        yaxis=dict(
            title="Detections",
            showgrid=True,
            gridcolor="#EEF2EE"
        )
    )

    chart.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        chart,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )

    # -----------------------------------------------------
    # Filter summary
    # -----------------------------------------------------

    total_detections = len(
        activities
    )

    if (
        selected_activity
        and selected_activity != "All Activities"
    ):

        st.caption(
            f"{total_detections} "
            f"detections for "
            f"{selected_activity}."
        )

    else:

        st.caption(
            f"{total_detections} "
            f"total activity detections."
        )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# STUDENT PERFORMANCE CHART
# =========================================================

def render_performance_chart(
    student_id=None
):

    activities = load_activity()

    # -----------------------------------------------------
    # No activity
    # -----------------------------------------------------

    if activities.empty:

        st.info(
            "No activity recorded yet."
        )

        return

    # -----------------------------------------------------
    # Filter by student
    # -----------------------------------------------------

    if student_id is not None:

        activities = activities[
            activities["student_id"].astype(str)
            == str(student_id)
        ]

    # -----------------------------------------------------
    # No student activity
    # -----------------------------------------------------

    if activities.empty:

        st.info(
            "No activity recorded for "
            "this student."
        )

        return

    # -----------------------------------------------------
    # Count activities
    # -----------------------------------------------------

    activity_counts = (
        activities["activity"]
        .value_counts()
        .reset_index()
    )

    activity_counts.columns = [
        "Activity",
        "Count"
    ]

    # -----------------------------------------------------
    # Calculate percentages
    # -----------------------------------------------------

    total = activity_counts[
        "Count"
    ].sum()

    if total == 0:

        st.info(
            "No activity data available."
        )

        return

    activity_counts[
        "Percentage"
    ] = (
        activity_counts["Count"]
        / total
        * 100
    )

    # -----------------------------------------------------
    # Panel
    # -----------------------------------------------------

    st.markdown(
        '<div class="panel">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="panel-title">'
        'Student Performance'
        '</div>',
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # Performance chart
    # -----------------------------------------------------

    chart = px.bar(
        activity_counts,
        x="Percentage",
        y="Activity",
        orientation="h",
        text="Percentage"
    )

    # Match the app's sage-green theme instead of Plotly's
    # default blue.
    chart.update_traces(
        marker_color="#6F9E87"
    )

    chart.update_layout(
        height=280,
        margin=dict(
            l=0,
            r=10,
            t=0,
            b=0
        ),
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Manrope",
            size=10,
            color="#8A948D"
        ),
        xaxis=dict(
            title="Percentage",
            range=[
                0,
                100
            ],
            showgrid=False
        ),
        yaxis=dict(
            title=""
        )
    )

    chart.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    st.plotly_chart(
        chart,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )
