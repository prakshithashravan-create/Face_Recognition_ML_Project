"""Unit tests for SQLite persistence behavior."""
import pytest

from src import database


@pytest.fixture
def db_path(tmp_path, monkeypatch):
    path = tmp_path / "test_attendance.db"
    monkeypatch.setattr(database, "DB_PATH", path)
    database.initialize_database()
    return path


def test_add_and_list_student(db_path):
    student_id = database.add_student(" Ada ", "Lovelace", "ada@example.test", "Computing", 2)
    students = database.list_students()

    assert len(students) == 1
    assert students[0]["student_id"] == student_id
    assert students[0]["first_name"] == "Ada"
    assert students[0]["last_name"] == "Lovelace"


def test_reject_blank_student_name(db_path):
    with pytest.raises(ValueError, match="required"):
        database.add_student(" ", "Lovelace")


def test_record_attendance_only_once_per_day(db_path):
    student_id = database.add_student("Grace", "Hopper")

    assert database.record_attendance(student_id, "Computer Science") is True
    assert database.record_attendance(student_id, "Computer Science") is False


def test_attendance_is_separate_by_subject(db_path):
    student_id = database.add_student("Katherine", "Johnson")

    assert database.record_attendance(student_id, "Maths") is True
    assert database.record_attendance(student_id, "Physics") is True


def test_reject_attendance_for_unknown_student(db_path):
    with pytest.raises(Exception):
        database.record_attendance(9999, "Maths")


def test_summary_returns_documented_ratio(db_path):
    first = database.add_student("Student", "One")
    second = database.add_student("Student", "Two")
    database.record_attendance(first, "Maths")

    attended, recorded_dates, ratio = database.attendance_summary(first, "Maths")
    assert attended == 1
    assert recorded_dates == 1
    assert ratio == 100.0

    assert database.record_attendance(second, "Maths") is False
