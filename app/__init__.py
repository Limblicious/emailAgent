from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()  # loads variables from .env into os.environ

# Now access it like:
api_key = os.getenv("OPENAI_API_KEY")


app = Flask(__name__)
CORS(app)

from . import routes  # noqa: E402,F401

__all__ = ["app"]
