import sys
import os

# Ensure the OpenAI client can initialize during tests
os.environ.setdefault("OPENAI_API_KEY", "test")
os.environ.setdefault("SMTP_HOST", "smtp.test")
os.environ.setdefault("SMTP_PORT", "25")
os.environ.setdefault("SMTP_EMAIL", "sender@test.com")
os.environ.setdefault("SMTP_PASSWORD", "password")

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
