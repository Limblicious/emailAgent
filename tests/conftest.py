import sys
import os

# Ensure the OpenAI client can initialize during tests
os.environ.setdefault("OPENAI_API_KEY", "test")

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
