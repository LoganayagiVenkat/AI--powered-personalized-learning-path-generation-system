import os
import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.app import create_app, logger

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    is_dev = os.getenv("FLASK_ENV", "development").lower() == "development"
    logger.info(f"Starting Python AI Learning Path backend server on http://localhost:{port} (debug={is_dev})")
    app.run(host="0.0.0.0", port=port, debug=is_dev, use_reloader=False)
