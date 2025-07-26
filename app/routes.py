from flask import jsonify, request, render_template

import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Ensure environment variables from a .env file are loaded
load_dotenv()

from . import app


@app.route('/')
def index():
    return jsonify({'message': 'Hello, World!'})


@app.route('/generate-flyer', methods=['POST'])
def generate_flyer():
    data = request.get_json()

    # Extract fields
    address = data.get('address', '')
    price = data.get('price', '')
    features = data.get('features', [])
    agent_name = data.get('agent_name', '')
    agent_phone = data.get('agent_phone', '')
    agent_email = data.get('agent_email', '')

    recipient_email = data.get('recipient_email', '').strip()

    html_body = data.get('html_body', '').strip()
    if not html_body:
        # Render flyer using Jinja2 if not provided in the payload
        html_body = render_template(
            'flyer_template.html',
            address=address,
            price=price,
            features=features,
            agent_name=agent_name,
            agent_phone=agent_phone,
            agent_email=agent_email
        )

    subject = data.get('subject', '').strip()
    if not subject:
        subject = f"Beautiful Home in {address.split(',')[0]} – Don’t Miss Out!"

    try:
        smtp_host = (os.getenv("SMTP_HOST") or "").strip()
        smtp_port = int((os.getenv("SMTP_PORT") or "587").strip())
        smtp_email = (os.getenv("SMTP_EMAIL") or "").strip()
        smtp_password = (os.getenv("SMTP_PASSWORD") or "").strip()

        msg = MIMEText(html_body, "html")
        msg["Subject"] = subject
        msg["From"] = smtp_email
        msg["To"] = recipient_email

        with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as server:
            server.starttls()
            server.login(smtp_email, smtp_password)
            server.sendmail(smtp_email, [recipient_email], msg.as_string())

        return jsonify({"status": "Email sent successfully", "subject": subject, "html_body": html_body}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

