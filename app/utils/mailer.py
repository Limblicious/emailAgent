import smtplib
import os
from email.message import EmailMessage


SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

if not all([SMTP_HOST, SMTP_PORT, SMTP_EMAIL, SMTP_PASSWORD]):
    raise RuntimeError(
        "Missing required SMTP configuration environment variables"
    )

SMTP_PORT = int(SMTP_PORT)

SENDER_EMAIL = SMTP_EMAIL
RECIPIENT_EMAIL = "recipient@example.com"
USERNAME = SMTP_EMAIL
PASSWORD = SMTP_PASSWORD


def send_flyer(subject: str, html_body: str) -> None:
    """Send the flyer via SMTP.

    Parameters
    ----------
    subject : str
        Email subject line.
    html_body : str
        HTML body of the email.
    """
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL
    msg.set_content(html_body, subtype="html")

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
            server.starttls()
            server.login(USERNAME, PASSWORD)
            server.send_message(msg)
        print("Email sent successfully")
    except Exception as exc:  # pragma: no cover - network failures expected
        print(f"Failed to send email: {exc}")
