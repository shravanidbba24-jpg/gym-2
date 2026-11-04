"""
Vercel Serverless Function Entry Point for Fitness Gym REST API.
Dispatches requests to the Flask WSGI instance defined in /app.py.
Includes WSGI path normalization for Vercel serverless rewrites.
"""

import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from app import app as flask_app

class VercelWSGIWrapper:
    """
    Normalizes WSGI environment PATH_INFO on Vercel so that Flask routes
    match whether Vercel passes `/api/health`, `/health`, or `/api/index.py/...`.
    """
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        path = environ.get("PATH_INFO", "")
        # Remove any leading script prefix added by Vercel serverless gateway
        for prefix in ("/api/index.py", "/index.py", "api/index.py", "index.py"):
            if path.startswith(prefix):
                path = path[len(prefix):]
                break
        if not path:
            path = "/"
        environ["PATH_INFO"] = path
        return self.wsgi_app(environ, start_response)

app = VercelWSGIWrapper(flask_app)
__all__ = ["app"]
