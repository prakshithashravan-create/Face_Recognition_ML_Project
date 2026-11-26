# Face Recognition Attendance Management System

A personal learning project exploring Python desktop development, computer vision, LBPH face recognition, and SQLite-based attendance records.

> **Project status:** Refactoring in progress. The original application is retained as `faceold.py` for reference. The modular implementation is under `src/`. The new implementation is educational and has not yet been validated with a complete real-world dataset or calibrated recognition threshold.

## Features in the refactored version

- Tkinter interface for student registration and viewing registered students.
- SQLite persistence with parameterized SQL statements and managed connections.
- Haar-cascade face detection and OpenCV LBPH recognition.
- Webcam-based attendance capture.
- Duplicate prevention: one attendance record per student, subject, and calendar date.
- Optional SMTP helper that reads credentials from environment variables rather than source code.
- Separate model-training script for locally supplied face images.

## Technology stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| OpenCV contrib | Haar-cascade detection and LBPH recognition |
| NumPy | Training labels and numerical data |
| Tkinter / ttk | Desktop interface |
| SQLite | Student and attendance storage |
| Pillow | Image handling dependency for future UI enhancements |
| SMTP | Optional email integration |

## Repository structure

```text
.
├── src/
│   ├── database.py       # SQLite schema and data access
│   ├── email_service.py  # Optional SMTP helper
│   ├── main.py           # Tkinter application
│   └── recognition.py    # Haar + LBPH recognition service
├── scripts/
│   └── train_model.py    # Train LBPH from local face images
├── assets/               # Add the Haar cascade XML here
├── dataset/              # Local training images (not committed)
├── models/               # Generated model files (not committed)
├── faceold.py            # Original implementation, retained for reference
├── requirements.txt
└── README.md
```

## Setup

### 1. Create and activate a virtual environment

**Windows (PowerShell):**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Add the Haar cascade

Create an `assets` folder and place the OpenCV Haar cascade file at:

```text
assets/haarcascade_frontalface_alt2.xml
```

### 3. Add training images

Create one folder per numeric student ID and add clear face images:

```text
dataset/
├── 1/
│   ├── image_01.jpg
│   └── image_02.jpg
└── 2/
    ├── image_01.jpg
    └── image_02.jpg
```

Use the same numeric IDs shown in the application's student list. Obtain consent before collecting or using anyone's face images. The dataset is intentionally excluded from Git.

### 4. Train the model

```powershell
python scripts/train_model.py
```

The script creates `models/trainer.yml`. The model is a local generated artifact and is not committed.

### 5. Run the application

From the repository root:

```powershell
python -m src.main
```

The SQLite database is created automatically at `data/attendance.db`.

## Optional email configuration

The SMTP helper is not yet wired into the Tkinter workflow. If you use it from your own integration, set credentials as environment variables instead of placing them in Python source:

```powershell
$env:SMTP_USERNAME="your-account@example.com"
$env:SMTP_PASSWORD="your-app-password"
```

Never commit real passwords, app passwords, API keys, student records, face images, or generated model files. If a real credential was previously committed, revoke or rotate it; deleting it from the latest version does not remove it from Git history.

## Important limitations

- LBPH's returned value is a distance-like score, not a probability. The default threshold is only a starting point and must be calibrated using representative test images.
- Lighting, camera quality, pose, and training-image quality affect recognition results. Unknown-person rejection must be tested carefully.
- The attendance percentage requires a proper class-session register to define how many sessions were held. The current schema records attendance dates only and should not be treated as an authoritative academic attendance calculation.
- The refactored app currently provides basic registration and attendance capture. Role-based admin/faculty authentication, profile management, attendance reporting, and integrated email alerts are not yet implemented in the new UI.
- This is a learning project, not a production biometric or access-control system. Apply consent, data minimization, secure storage, retention, and access controls before any real deployment.

## Learning outcomes

- Building a Python desktop interface with Tkinter.
- Separating database, recognition, and UI responsibilities into modules.
- Using SQLite parameterized queries and transaction handling.
- Exploring Haar-cascade detection and LBPH face recognition.
- Training a basic recognition model from local image data.
- Managing configuration and secrets outside source code.

## Original implementation

`faceold.py` is retained as a legacy reference. Prefer the modular `src/` implementation for further development. The original version has known design and reliability limitations and should not be treated as production-ready.
