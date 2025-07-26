from flask import jsonify, request, render_template

import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Ensure environment variables from a .env file are loaded
load_dotenv()

# ``app`` is defined in the top-level ``app.py`` module
from app import app


@app.route('/')
def index():
    """Render the main flyer form."""
    return render_template("form.html")


@app.route('/flyer-form')
def flyer_form():
    """Serve a simple HTML form for generating flyers."""
    return render_template(
        'flyer_form.html',
        message=None,
        error=None,
        form_data={},
        error_fields=[]
    )


@app.route('/generate-flyer', methods=['POST'])
def generate_flyer():
    """Generate a flyer email from JSON or form data."""

    if request.is_json:
        data = request.get_json() or {}
        from_form = False
    else:
        data = request.form.to_dict()
        from_form = True

    # Normalize features so it can be provided as a list or newline-delimited string
    features_value = data.get('features', [])
    if isinstance(features_value, str):
        features_value = [f.strip() for f in features_value.splitlines() if f.strip()]
    data['features'] = features_value

    if from_form:
        required_fields = ['address', 'price', 'features', 'agent_name', 'agent_phone', 'agent_email', 'subject']
        missing_fields = [f for f in required_fields if not data.get(f) or (f == 'features' and not features_value)]
        if missing_fields:
            return render_template(
                'flyer_form.html',
                error='Please fill out all fields.',
                message=None,
                error_fields=missing_fields,
                form_data=data
            )

    # Extract fields
    address = data.get('address', '')
    price = data.get('price', '')
    features = data.get('features', [])
    agent_name = data.get('agent_name', '')
    agent_phone = data.get('agent_phone', '')
    agent_email = data.get('agent_email', '')

    recipient_email = data.get('recipient_email', '').strip() or agent_email.strip()

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

        if from_form:
            return render_template(
                'flyer_form.html',
                message='Email sent successfully',
                error=None,
                form_data={},
                error_fields=[]
            )
        return jsonify({"status": "Email sent successfully", "subject": subject, "html_body": html_body}), 200
    except Exception as e:
        if from_form:
            return render_template(
                'flyer_form.html',
                message=f"Error: {e}",
                error=None,
                form_data={},
                error_fields=[]
            )
        return jsonify({"error": str(e)}), 500

