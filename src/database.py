"""SQLite persistence for student records and attendance."""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "attendance.db"


@contextmanager
def connection() -> Iterator[sqlite3.Connection]:
    """Yield a transactional SQLite connection with foreign keys enabled."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def initialize_database() -> None:
    """Create the application schema when it does not already exist."""
    with connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT,
                course TEXT,
                year INTEGER,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS attendance (
                attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL REFERENCES students(student_id),
                subject TEXT NOT NULL,
                attendance_date TEXT NOT NULL DEFAULT (date('now','localtime')),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(student_id, subject, attendance_date)
            );
            """
        )


def add_student(
    first_name: str,
    last_name: str,
    email: str = "",
    course: str = "",
    year: int | None = None,
) -> int:
    """Create a student and return the generated numeric ID."""
    first_name, last_name = first_name.strip(), last_name.strip()
    if not first_name or not last_name:
        raise ValueError("First name and last name are required.")
    if year is not None and year < 1:
        raise ValueError("Year must be a positive integer.")
    with connection() as conn:
        cursor = conn.execute(
            "INSERT INTO students(first_name,last_name,email,course,year) VALUES(?,?,?,?,?)",
            (first_name, last_name, email.strip(), course.strip(), year),
        )
        return int(cursor.lastrowid)


def list_students() -> list[sqlite3.Row]:
    """Return students ordered by their numeric ID."""
    with connection() as conn:
        return list(conn.execute("SELECT * FROM students ORDER BY student_id"))


def record_attendance(student_id: int, subject: str) -> bool:
    """Record one attendance per student, subject, and calendar date.

    Returns False if a matching record already exists for today.
    """
    subject = subject.strip()
    if not subject:
        raise ValueError("Subject is required.")
    with connection() as conn:
        cursor = conn.execute(
            "INSERT OR IGNORE INTO attendance(student_id, subject) VALUES(?,?)",
            (student_id, subject),
        )
        return cursor.rowcount == 1


def attendance_summary(student_id: int, subject: str) -> tuple[int, int, float]:
    """Return attended dates, dates with any attendance, and their ratio.

    This is a descriptive ratio, not an academic attendance percentage:
    a separate class-session register is required for that calculation.
    """
    with connection() as conn:
        attended = conn.execute(
            "SELECT COUNT(*) FROM attendance WHERE student_id=? AND subject=?",
            (student_id, subject),
        ).fetchone()[0]
        sessions = conn.execute(
            "SELECT COUNT(DISTINCT attendance_date) FROM attendance WHERE subject=?",
            (subject,),
        ).fetchone()[0]
    percentage = (attended / sessions * 100.0) if sessions else 0.0
    return int(attended), int(sessions), percentage
