"""SQLite persistence for students and attendance records."""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "attendance.db"


@contextmanager
def connection() -> Iterator[sqlite3.Connection]:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def initialize_database() -> None:
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


def add_student(first_name: str, last_name: str, email: str = "", course: str = "", year: int | None = None) -> int:
    with connection() as conn:
        cursor = conn.execute(
            "INSERT INTO students(first_name,last_name,email,course,year) VALUES(?,?,?,?,?)",
            (first_name.strip(), last_name.strip(), email.strip(), course.strip(), year),
        )
        return int(cursor.lastrowid)


def list_students() -> list[sqlite3.Row]:
    with connection() as conn:
        return list(conn.execute("SELECT * FROM students ORDER BY student_id"))


def record_attendance(student_id: int, subject: str) -> bool:
    """Record one attendance per student, subject and calendar date.

    Returns False when that attendance already exists for today.
    """
    with connection() as conn:
        cursor = conn.execute(
            "INSERT OR IGNORE INTO attendance(student_id, subject) VALUES(?,?)",
            (student_id, subject.strip()),
        )
        return cursor.rowcount == 1


def attendance_summary(student_id: int, subject: str) -> tuple[int, int, float]:
    """Return attended sessions, recorded sessions, and percentage.

    The denominator is the number of distinct attendance dates recorded for
    the subject in this database; a timetable/session register is needed for
    an authoritative percentage.
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
