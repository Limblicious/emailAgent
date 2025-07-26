import smtplib
from email.message import EmailMessage


SMTP_HOST = "smtp.example.com"
SMTP_PORT = 587
SENDER_EMAIL = "noreply@example.com"
RECIPIENT_EMAIL = "recipient@example.com"
USERNAME = "noreply@example.com"
PASSWORD = "examplepassword"


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
