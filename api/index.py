"""
Vercel Serverless Function Entry Point for Fitness Gym REST API.
Dispatches requests to the Flask WSGI instance defined in /app.py.
"""

import sys
import os

# Add root directory to python module search path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from app import app

# Export the WSGI app for @vercel/python runtime
# Vercel's Python builder automatically uses 'app' as the WSGI callable.
__all__ = ["app"]
