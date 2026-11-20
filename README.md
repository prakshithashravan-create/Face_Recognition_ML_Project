# Face Recognition Based Attendance Management System

## Project Overview

The Face Recognition Based Attendance Management System is a Python desktop application developed as a personal learning project to explore computer vision, machine learning, and database integration.

The application uses facial recognition technology to identify students and automate attendance tracking. It provides separate access for administrators and faculty members, allowing student registration, attendance management, attendance status monitoring, and email notifications.

The project aims to reduce manual attendance tracking and demonstrate how Python and OpenCV can be used to build practical real-world applications.

## Key Features

- **Admin Login:** Secure login interface for administrators.
- **Faculty Login:** Separate login functionality for faculty members.
- **Student Registration:** Add and store student information in an SQLite database.
- **Face Recognition:** Detect and recognize student faces using OpenCV and the LBPH algorithm.
- **Automated Attendance:** Record student attendance based on facial recognition.
- **Attendance Monitoring:** View attendance status for individual students and subjects.
- **Attendance Percentage:** Calculate attendance percentages based on recorded classes.
- **Email Notifications:** Send email alerts to parents when a student's attendance falls below the defined 75% threshold.

## Technologies Used

| Technology | Application |
|---|---|
| Python | Application development |
| OpenCV | Face detection and recognition |
| LBPH | Face recognition algorithm |
| NumPy | Numerical processing |
| Tkinter | Graphical User Interface |
| SQLite3 | Database management |
| Pillow | Image processing |
| Pickle | Face label serialization |
| SMTP | Email notifications |

## Application Workflow

1. Administrator or faculty member logs into the application.
2. Administrator registers student details.
3. The face recognition model identifies students through a webcam.
4. Recognized students have their attendance updated in the database.
5. Faculty members can check attendance percentages for different subjects.
6. Email notifications can be sent when attendance falls below the defined threshold.

## Project Structure

```text
Face-Recognition-Attendance-System/
│
├── faceold.py
├── requirements.txt
├── README.md
│
├── cascade/
│   └── data/
│       └── haarcascade_frontalface_alt2.xml
│
├── models/
│   ├── trainer.yml
│   └── labels.pickle
│
└── screenshots/
    └── application_screenshot.png
```

*Note: The cascade classifier and trained model files are external dependencies referenced by the application. Add them only if you have the appropriate files and permission to share them.*

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/Face-Recognition-Attendance-System.git
```

### 2. Navigate to the project directory

```bash
cd Face-Recognition-Attendance-System
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the required files

Ensure the Haar Cascade XML file, trained LBPH model, and face label file are available in their expected locations.

Initialize the SQLite database with the required tables before running the application.

### 5. Run the application

```bash
python faceold.py
```

## Learning Outcomes

Through this project, I explored:

- Python desktop application development using Tkinter.
- Face detection and recognition using OpenCV.
- Fundamentals of the LBPH face recognition algorithm.
- Integration of Python applications with SQLite databases.
- Image processing and webcam integration.
- Email communication using SMTP.
- Connecting multiple Python libraries to develop an end-to-end application.

## Project Purpose

This project was developed independently for learning and practical exploration of Python programming, computer vision, and machine learning concepts.

**Disclaimer:** This is an educational project and is not intended for production deployment. Face recognition accuracy, biometric data privacy, authentication security, and email credential management require additional improvements before real-world use.
