from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from . import routes  # noqa: E402,F401

__all__ = ["app"]
