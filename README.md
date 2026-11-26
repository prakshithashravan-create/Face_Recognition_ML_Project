# Face Recognition Attendance Management System

A Python desktop application that explores face detection, LBPH-based face recognition, and attendance tracking with SQLite. Built as a hands-on learning project using OpenCV and Tkinter.

[![CI](https://github.com/prakshithashravan-create/Face_Recognition_ML_Project/actions/workflows/ci.yml/badge.svg)](https://github.com/prakshithashravan-create/Face_Recognition_ML_Project/actions/workflows/ci.yml)

## Project overview

The application provides a small desktop workflow to register students, train a local face-recognition model from consented sample images, and record attendance against a subject. The code is organized into separate UI, recognition, training, and persistence modules.

**Project maturity:** portfolio / learning project. The automated tests cover database behavior. The webcam and recognition workflow still requires local validation with a real camera and representative images; the recognition threshold is configurable and has not been scientifically calibrated. This is not a production biometric or access-control system.

## Features

- Student registration and student-list view through a Tkinter desktop UI.
- SQLite persistence with parameterized queries, transaction handling, and referential integrity.
- Haar-cascade face detection and OpenCV LBPH recognition.
- Local model training from images organized by numeric student ID.
- Webcam-based attendance capture with duplicate prevention per student, subject, and date.
- SMTP helper that reads credentials from environment variables (not embedded in source).
- Automated database unit tests and GitHub Actions CI.

## Architecture

```text
src/
  main.py             Tkinter user interface and application flow
  database.py         SQLite schema and data-access functions
  recognition.py      Haar detection and LBPH prediction
  email_service.py    Optional SMTP utility
scripts/
  train_model.py      Local LBPH model-training command
tests/
  test_database.py    Database behavior tests
assets/               Local Haar cascade XML (not committed)
dataset/              Local face images (not committed)
models/               Generated LBPH model (not committed)
```

The UI calls the database and recognition modules; model training is a separate command. Local biometric images and generated model files are deliberately excluded from version control.

## Technology stack

| Technology | Use |
|---|---|
| Python 3.10+ | Application and tooling |
| OpenCV contrib | Haar cascade and LBPH face recognition |
| NumPy | Training labels and image arrays |
| Tkinter / ttk | Desktop user interface |
| SQLite | Local relational data storage |
| pytest | Automated database tests |
| GitHub Actions | Continuous integration |

## Quick start (Windows)

1. Install Python 3.10 or newer.
2. Clone the repository and open a terminal in its root directory.
3. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. Download the OpenCV Haar cascade XML file and place it at `assets/haarcascade_frontalface_alt2.xml`.
5. Add consented training images as described below.
6. Train the model and start the application:

   ```powershell
   python scripts/train_model.py
   python -m src.main
   ```

The SQLite database is initialized automatically at `data/attendance.db`.

## Prepare the training dataset

Create one directory per numeric student ID. Use the same ID generated when registering the student in the application.

```text
dataset/
  1/
    sample_01.jpg
    sample_02.jpg
  2/
    sample_01.jpg
    sample_02.jpg
```

Use clear, varied images with one face per image. The training script detects the largest face in each image and skips unreadable images or images with no detected face. Obtain explicit consent before collecting or processing face images. Do not upload face images, student records, database files, or trained model artifacts to this public repository.

## Run tests

```powershell
pytest -q
```

The test suite verifies database initialization, student creation, duplicate attendance prevention, and attendance summary behavior. It does not validate camera hardware or recognition accuracy.

## Configuration

The optional SMTP helper reads these environment variables:

- `SMTP_HOST` (defaults to `smtp.gmail.com`)
- `SMTP_PORT` (defaults to `587`)
- `SMTP_USERNAME`
- `SMTP_PASSWORD`

Email sending is not currently connected to the desktop UI. Use an app-specific password or an approved SMTP credential; never commit secrets.

## Design decisions

- **Separation of concerns:** UI, persistence, recognition, and model training are kept in distinct modules.
- **Parameterized SQL:** user-provided values are passed as query parameters.
- **Local-first data:** SQLite, images, and model artifacts stay on the user's machine by default.
- **Duplicate protection:** a database uniqueness constraint prevents repeated attendance rows for the same student, subject, and date.
- **Explicit limitations:** attendance percentages are not calculated because the current schema has no authoritative class-session register.

## Known limitations and next steps

- No admin/faculty authentication or role-based access control.
- No in-app image capture / dataset enrollment workflow; training images are prepared locally.
- No session timetable, so attendance percentages and absence calculations are intentionally not presented.
- No email-alert workflow in the UI.
- LBPH thresholds need calibration and evaluation against false-accept / false-reject cases.
- Biometric data needs a formal consent, retention, encryption, and access-control design before any real deployment.

## Privacy and security

This project handles biometric data, which is sensitive. Use only images for which you have permission. Keep the dataset, SQLite database, and trained model on a secured local machine. The repository ignores these files by default. Do not use this project to make consequential decisions about people.

If a credential was ever committed to Git history, rotating or revoking it is necessary; removing it from the latest file does not erase it from earlier commits.

## About

Created as a personal learning project to practice Python application development, computer vision, database operations, and modular code organization.
