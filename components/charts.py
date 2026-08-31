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

BAHRAIN_TIMEZONE = ZoneInfo("Asia/Bahrain")


# =========================================================
# FIXED ACTIVITY CLASSES
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
