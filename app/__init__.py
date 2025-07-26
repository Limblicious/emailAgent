from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from a .env file if present.
load_dotenv()


app = Flask(__name__)
CORS(app)

from . import routes  # noqa: E402,F401

__all__ = ["app"]
