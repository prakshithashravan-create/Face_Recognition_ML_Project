"""OpenCV Haar-cascade and LBPH face-recognition helpers."""
from __future__ import annotations

from pathlib import Path

import cv2

ROOT = Path(__file__).resolve().parents[1]
CASCADE_PATH = ROOT / "assets" / "haarcascade_frontalface_alt2.xml"
MODEL_PATH = ROOT / "models" / "trainer.yml"


class FaceRecognizer:
    """Load the local cascade/model and classify cropped grayscale faces."""

    def __init__(self, threshold: float = 65.0) -> None:
        if threshold <= 0:
            raise ValueError("Recognition threshold must be greater than zero.")
        if not hasattr(cv2, "face"):
            raise RuntimeError(
                "OpenCV LBPH is unavailable. Install opencv-contrib-python, "
                "not the standard opencv-python package."
            )
        if not CASCADE_PATH.is_file():
            raise FileNotFoundError(f"Haar cascade not found: {CASCADE_PATH}")
        if not MODEL_PATH.is_file():
            raise FileNotFoundError(
                f"Trained model not found: {MODEL_PATH}. Run scripts/train_model.py first."
            )

        self.cascade = cv2.CascadeClassifier(str(CASCADE_PATH))
        if self.cascade.empty():
            raise RuntimeError("OpenCV could not load the Haar cascade file.")
        self.model = cv2.face.LBPHFaceRecognizer_create()
        self.model.read(str(MODEL_PATH))
        self.threshold = threshold

    def detect(self, frame):
        """Return a grayscale frame and detected face bounding boxes."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.cascade.detectMultiScale(
            gray, scaleFactor=1.2, minNeighbors=5, minSize=(60, 60)
        )
        return gray, faces

    def predict(self, gray_face):
        """Return (student_id, distance); unknown faces return (None, distance)."""
        if gray_face is None or gray_face.size == 0:
            return None, float("inf")
        normalized = cv2.resize(gray_face, (200, 200))
        label, distance = self.model.predict(normalized)
        # LBPH returns a distance-like score: lower is a closer match.
        if distance <= self.threshold:
            return int(label), float(distance)
        return None, float(distance)
