# emailAgent

This repository contains a simple Flask application template with an example route and utilities for interacting with OpenAI.

## Setup

Install the required packages using pip:

```bash
pip install -r requirements.txt
```

Run the Flask application in development mode:

```bash
flask run --app app.py
```

## Production

To run the application with Gunicorn, first install it:

```bash
pip install gunicorn
```

Then start the server bound to port 5000:

```bash
gunicorn app:app --bind 0.0.0.0:5000
```

## Testing

Run tests with `pytest`:

```bash
pytest
```
