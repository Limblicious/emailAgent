from flask import jsonify, request
from .utils.openai_client import generate_flyer

from . import app


@app.route('/')
def index():
    return jsonify({'message': 'Hello, World!'})


@app.route('/generate-flyer', methods=['POST'])
def generate_flyer_route():
    """Generate an email flyer based on property details."""
    data = request.get_json(silent=True) or {}

    required_fields = [
        "address",
        "price",
        "features",
        "agent_name",
        "agent_phone",
        "agent_email",
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    result = generate_flyer({key: data[key] for key in required_fields})
    return jsonify({
        "subject": result.get("subject", ""),
        "html_body": result.get("html_body", ""),
    })
