from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from a .env file if present.
load_dotenv()

# The templates reside inside ``app_pkg/templates`` so we provide the path
app = Flask(__name__, template_folder="app_pkg/templates")
CORS(app)

# Import routes after the app is created so they can register with it
from app_pkg import routes  # noqa: E402,F401

__all__ = ["app"]

if __name__ == "__main__":  # pragma: no cover - manual development mode
    app.run(debug=True)
