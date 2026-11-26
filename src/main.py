"""Tkinter front end for student registration and face-based attendance."""
from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

import cv2

from src.database import add_student, initialize_database, list_students, record_attendance
from src.recognition import FaceRecognizer


class AttendanceApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Face Recognition Attendance")
        self.geometry("760x560")
        self.minsize(680, 480)
        initialize_database()
        self._build_ui()
        self.refresh_students()

    def _build_ui(self) -> None:
        container = ttk.Frame(self, padding=18)
        container.pack(fill="both", expand=True)
        ttk.Label(container, text="Face Recognition Attendance", font=("Segoe UI", 18, "bold")).pack(anchor="w")
        ttk.Label(container, text="Register students and record one attendance per subject per day.").pack(anchor="w", pady=(2, 16))

        form = ttk.LabelFrame(container, text="Student registration", padding=12)
        form.pack(fill="x")
        self.first = tk.StringVar()
        self.last = tk.StringVar()
        self.email = tk.StringVar()
        self.course = tk.StringVar()
        self.year = tk.StringVar()
        fields = [("First name", self.first), ("Last name", self.last), ("Email", self.email), ("Course", self.course), ("Year", self.year)]
        for index, (label, variable) in enumerate(fields):
            row, col = divmod(index, 3)
            ttk.Label(form, text=label).grid(row=row * 2, column=col, sticky="w", padx=6, pady=(4, 0))
            ttk.Entry(form, textvariable=variable, width=24).grid(row=row * 2 + 1, column=col, sticky="ew", padx=6, pady=(0, 8))
        for col in range(3):
            form.columnconfigure(col, weight=1)
        ttk.Button(form, text="Register student", command=self.register_student).grid(row=4, column=0, sticky="w", padx=6, pady=4)

        attendance = ttk.LabelFrame(container, text="Take attendance", padding=12)
        attendance.pack(fill="x", pady=14)
        self.subject = tk.StringVar(value="s1")
        ttk.Label(attendance, text="Subject").pack(side="left")
        ttk.Entry(attendance, textvariable=self.subject, width=18).pack(side="left", padx=8)
        ttk.Button(attendance, text="Start webcam", command=self.take_attendance).pack(side="left", padx=8)
        ttk.Label(attendance, text="Press Q in the camera window to stop.").pack(side="left", padx=8)

        listing = ttk.LabelFrame(container, text="Registered students", padding=10)
        listing.pack(fill="both", expand=True)
        self.students = ttk.Treeview(listing, columns=("id", "name", "course", "year"), show="headings", height=8)
        for key, label, width in [("id", "Student ID", 90), ("name", "Name", 220), ("course", "Course", 160), ("year", "Year", 90)]:
            self.students.heading(key, text=label)
            self.students.column(key, width=width)
        self.students.pack(fill="both", expand=True)
        ttk.Button(container, text="Refresh list", command=self.refresh_students).pack(anchor="e", pady=(8, 0))

    def register_student(self) -> None:
        first, last = self.first.get().strip(), self.last.get().strip()
        if not first or not last:
            messagebox.showwarning("Missing details", "Please enter first and last name.")
            return
        try:
            year_text = self.year.get().strip()
            year = int(year_text) if year_text else None
            student_id = add_student(first, last, self.email.get(), self.course.get(), year)
        except ValueError:
            messagebox.showerror("Invalid year", "Year must be a whole number.")
            return
        except Exception as exc:
            messagebox.showerror("Registration failed", str(exc))
            return
        messagebox.showinfo("Student registered", f"Student ID: {student_id}\nUse this numeric ID as the folder name under dataset/ before training the model.")
        for variable in (self.first, self.last, self.email, self.course, self.year):
            variable.set("")
        self.refresh_students()

    def refresh_students(self) -> None:
        for item in self.students.get_children():
            self.students.delete(item)
        for student in list_students():
            name = f"{student['first_name']} {student['last_name']}"
            self.students.insert("", "end", values=(student["student_id"], name, student["course"] or "", student["year"] or ""))

    def take_attendance(self) -> None:
        subject = self.subject.get().strip()
        if not subject:
            messagebox.showwarning("Subject required", "Enter a subject name first.")
            return
        try:
            recognizer = FaceRecognizer()
        except Exception as exc:
            messagebox.showerror("Recognition setup", str(exc))
            return
        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            camera.release()
            messagebox.showerror("Camera unavailable", "Could not open webcam. Check camera permissions and try again.")
            return
        recorded_today: set[int] = set()
        try:
            while True:
                ok, frame = camera.read()
                if not ok:
                    raise RuntimeError("Could not read a frame from the webcam.")
                gray, faces = recognizer.detect(frame)
                for x, y, width, height in faces:
                    face = gray[y:y + height, x:x + width]
                    student_id, distance = recognizer.predict(face)
                    if student_id is not None:
                        if student_id not in recorded_today:
                            created = record_attendance(student_id, subject)
                            recorded_today.add(student_id)
                            status = "Recorded" if created else "Already marked today"
                        else:
                            status = "Already processed"
                        label = f"ID {student_id}: {status} ({distance:.1f})"
                    else:
                        label = f"Unknown ({distance:.1f})"
                    cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 180, 0) if student_id is not None else (0, 0, 220), 2)
                    cv2.putText(frame, label, (x, max(20, y - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)
                cv2.imshow("Attendance - press Q to stop", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
        except Exception as exc:
            messagebox.showerror("Attendance error", str(exc))
        finally:
            camera.release()
            cv2.destroyAllWindows()
            self.refresh_students()


if __name__ == "__main__":
    AttendanceApp().mainloop()
