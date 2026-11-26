"""Optional SMTP email helper; credentials are read from environment variables."""
from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage


def send_email(recipient: str, subject: str, body: str) -> None:
    host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    port = int(os.getenv("SMTP_PORT", "587"))
    sender = os.getenv("SMTP_USERNAME")
    password = os.getenv("SMTP_PASSWORD")
    if not sender or not password:
        raise RuntimeError("Set SMTP_USERNAME and SMTP_PASSWORD environment variables first.")

    message = EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)
    with smtplib.SMTP(host, port, timeout=20) as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(message)
