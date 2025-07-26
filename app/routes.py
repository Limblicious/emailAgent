from flask import jsonify, request, render_template

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

    # Render flyer using Jinja2
    html_body = render_template(
        'flyer_template.html',
        address=address,
        price=price,
        features=features,
        agent_name=agent_name,
        agent_phone=agent_phone,
        agent_email=agent_email
    )

    subject = f"Beautiful Home in {address.split(',')[0]} – Don’t Miss Out!"
    return jsonify({"subject": subject, "html_body": html_body})

