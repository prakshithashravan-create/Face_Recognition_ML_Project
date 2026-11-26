"""Train an LBPH model from dataset/<numeric_student_id> image folders."""
from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "dataset"
CASCADE = ROOT / "assets" / "haarcascade_frontalface_alt2.xml"
OUTPUT = ROOT / "models" / "trainer.yml"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp"}


def main() -> None:
    if not hasattr(cv2, "face"):
        raise RuntimeError("Install opencv-contrib-python to train an LBPH model.")
    if not DATASET.is_dir():
        raise FileNotFoundError(f"Dataset directory not found: {DATASET}")
    if not CASCADE.is_file():
        raise FileNotFoundError(f"Missing Haar cascade: {CASCADE}")

    detector = cv2.CascadeClassifier(str(CASCADE))
    if detector.empty():
        raise RuntimeError(f"Could not load Haar cascade: {CASCADE}")

    faces: list[np.ndarray] = []
    labels: list[int] = []
    for student_dir in sorted(path for path in DATASET.iterdir() if path.is_dir()):
        if not student_dir.name.isdigit():
            print(f"Skipping folder with non-numeric student ID: {student_dir.name}")
            continue
        for image_path in sorted(student_dir.iterdir()):
            if image_path.suffix.lower() not in IMAGE_EXTENSIONS:
                continue
            image = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
            if image is None:
                print(f"Skipping unreadable image: {image_path}")
                continue
            detected = detector.detectMultiScale(
                image, scaleFactor=1.2, minNeighbors=5, minSize=(60, 60)
            )
            if len(detected) == 0:
                print(f"No face detected; skipping: {image_path.name}")
                continue
            x, y, width, height = max(detected, key=lambda box: box[2] * box[3])
            face = image[y : y + height, x : x + width]
            faces.append(cv2.resize(face, (200, 200)))
            labels.append(int(student_dir.name))

    if not faces:
        raise RuntimeError("No usable face images found under dataset/<student_id>/.")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces, np.asarray(labels, dtype=np.int32))
    recognizer.write(str(OUTPUT))
    print(
        f"Saved model with {len(faces)} face samples "
        f"for {len(set(labels))} students: {OUTPUT}"
    )


if __name__ == "__main__":
    main()
