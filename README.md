# 🌿 BASMA — AI Classroom Analytics

BASMA is an AI-powered classroom analytics system designed to help teachers monitor student attendance and classroom activities using Computer Vision.

The system combines **Face Recognition** for student identification with **YOLO-based activity detection** to analyze classroom images and generate attendance and activity insights.

---

## 🌐 Live Demo

Try BASMA online:

https://basmaclassa.streamlit.app/

---

## ✨ Features

### 👤 Student Registration

Teachers can register students before starting classroom monitoring.

Each student can be registered with:

- Student ID
- Student Name
- Parent Email
- Parent Phone
- Student Photo

The student photo is used to generate a face embedding for later student recognition.

---

### 📸 Live Classroom

The Live Classroom page allows the teacher to use the device camera to capture a classroom image.

After taking a classroom photo, BASMA analyzes the image to:

- Detect registered students
- Recognize students using Face Recognition
- Detect classroom activities using YOLO
- Record attendance
- Record detected classroom activities

```text
Open Camera
     ↓
Capture Classroom Image
     ↓
Face Recognition + YOLO
     ↓
Student Identification
     +
Activity Detection
     ↓
Attendance & Activity Records
````

---

## 🤖 Classroom Activity Detection

BASMA uses a trained YOLO model to detect classroom activities.

The current model supports **8 classroom activities**:

* 👏 Clapping
* 🧍 Facing-Forward
* 🙋 Hand-Raising
* 📖 Reading
* 😴 Sleeping
* 💬 Talking
* 📱 Using-Phone
* ✍️ Writing

---

# 🧠 How BASMA Works

```text
Student Registration
        ↓
Student Photo
        ↓
Face Embedding
        ↓
Registered Student Data
        ↓
Open Classroom Camera
        ↓
Capture Classroom Image
        ↓
 ┌───────────────────────┐
 │                       │
 ▼                       ▼
Face Recognition        YOLO
 │                       │
 ▼                       ▼
Student Identity      Activity Detection
 │                       │
 └───────────┬───────────┘
             ↓
     Attendance & Activity
             ↓
       Classroom Analytics
             ↓
      Reports & Insights
```

---

# 📊 Dashboard

The BASMA Dashboard provides an overview of classroom activity and attendance.

### Dashboard Filters

Teachers can filter the dashboard by:

* Student
* Activity

### Classroom Overview

The dashboard displays:

* Total Students
* Present Today
* Attendance Rate
* Activity Detections

### Classroom Insights

The dashboard includes:

* 🎯 Class Activity
* 👥 Attendance
* 📈 Student Performance

### Data Downloads

Teachers can download:

* Attendance data
* Activity data
* Student data

---

# 👤 Student Profile

The Student Profile section provides student-specific information based on registered students and recorded classroom data.

Student profiles become available after students are registered in BASMA.

---

# 📈 Analytics

The Analytics page provides classroom insights based on the collected attendance and activity records.

It includes:

### 🎯 Class Activity

Displays detected classroom activities.

### 👥 Attendance

Displays student attendance information.

### 📈 Student Performance

Provides student-level classroom insights based on the available data.

---

# 📋 Reports

BASMA provides a dedicated Reports section for generating classroom reports.

Teachers can select a reporting date and view:

* Attendance Records
* Activity Detections
* Attendance Preview
* Activity Preview

Reports can be downloaded for further use.

---

# 📧 Email Attendance Report

BASMA supports sending attendance reports by email.

The teacher can enter a recipient email address and send the attendance report directly from the application.

---

# 📊 Google Sheets

BASMA supports synchronizing attendance and classroom activity records with Google Sheets.

This allows classroom data to be stored and managed externally for easier access and organization.

---

# ⚙️ Settings

The Settings page allows teachers to customize the dashboard.

Teachers can choose which dashboard sections are displayed:

* Show Metric Cards
* Show Class Activity
* Show Attendance
* Show Student Profile
* Show Student Performance

The Settings page also provides system information, including:

* BASMA AI Classroom Analytics
* YOLO classroom activity detection status
* Bahrain timezone (UTC+3)

---

# 🛠️ Technologies

BASMA is built using:

* Python
* Streamlit
* Ultralytics YOLO
* InsightFace
* OpenCV
* Pandas
* NumPy
* Plotly
* Google Sheets API
* SMTP Email

---

# 🧩 AI Components

## YOLO — Activity Detection

YOLO is used to detect classroom activities from captured classroom images.

```text
Classroom Image
      ↓
     YOLO
      ↓
Activity Detection
      ↓
Activity Records
```

---

## Face Recognition — Student Identification

Face Recognition is used to identify registered students.

```text
Student Photo
      ↓
Face Detection
      ↓
Face Embedding
      ↓
Student Embedding
      ↓
Classroom Image
      ↓
Face Matching
      ↓
Student Identity
```

The recognized student information is then used for attendance tracking.

---

# 📁 Project Structure

```text
basma/
│
├── app.py
├── README.md
├── requirements.txt
│
├── assets/
│
├── components/
│   ├── cards.py
│   ├── charts.py
│   ├── live_classroom.py
│   ├── sidebar.py
│   ├── student_profile.py
│   └── student_registration.py
│
├── data/
│   ├── students.csv
│   ├── attendance.csv
│   └── activity_log.csv
│
├── models/
│   └── basma_yolo.pt
│
├── styles/
│   └── basma_theme.css
│
└── utils/
    ├── activity_detection.py
    ├── attendance.py
    ├── data_manager.py
    ├── email_utils.py
    ├── face_utils.py
    ├── google_sheets.py
    └── report_utils.py
```

The repository also contains the project's final notebook:

```text
Basma_notebook_final.ipynb
```

---

# 📂 Data

BASMA uses CSV files to store classroom information.

## Students

```text
student_id
student_name
parent_email
parent_phone
photo_path
```

## Attendance

```text
student_id
date
first_seen
last_seen
status
```

## Activity Log

```text
student_id
date
time
activity
```

---

# 🚀 Installation

## 1. Clone the repository

```bash
git clone https://github.com/fatema-madan04/basma.git
```

## 2. Open the project

```bash
cd basma
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Run BASMA

```bash
streamlit run app.py
```

The application will then open in your browser.

---

# ⚙️ Configuration

Some BASMA features require external configuration, including:

* Google Sheets
* Email services

Sensitive credentials should be stored securely using Streamlit Secrets or environment variables.

Do not commit passwords, API keys, service-account credentials, or other secrets to the repository.

---

# 🎯 Project Goal

BASMA aims to transform classroom observations into useful data that can help teachers understand:

* 👥 Student attendance
* 🎯 Classroom activities
* 📊 Student performance
* 📈 Classroom activity patterns
* 🤖 AI-based classroom insights

Instead of manually recording attendance and classroom activities, BASMA uses Computer Vision to automate the process.

---

# 🔬 AI Pipeline

BASMA combines two Computer Vision tasks:

```text
              Classroom Image
                     │
          ┌──────────┴──────────┐
          │                     │
          ▼                     ▼
   Face Recognition            YOLO
          │                     │
          ▼                     ▼
 Student Identification    Activity Detection
          │                     │
          ▼                     ▼
      Attendance          Activity Records
          │                     │
          └──────────┬──────────┘
                     ▼
              Classroom Analytics
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
      Dashboard   Reports   Student Profile
```

---

# 🌱 Project Status

**Prototype / Capstone Project**

BASMA is a Computer Vision and Data Science capstone project focused on applying AI to classroom attendance and activity analytics.

---

# 🔮 Future Improvements

Possible future improvements include:

* Real-time continuous classroom monitoring
* More classroom activity classes
* Improved multi-student tracking
* Improved face recognition under challenging lighting
* More advanced student performance analytics
* More detailed engagement reports
* Automated parent notifications
* Support for longer classroom sessions

---

# 🌿 BASMA

**AI-powered classroom analytics through Computer Vision.**
