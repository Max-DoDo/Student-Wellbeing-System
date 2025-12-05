#!/usr/bin/env python3
"""
Main entry point for the Student Wellbeing System.
Run this file from the project root to start the application.
"""
import sys
import os
import logging

# Add src directory to Python path so that 'base' module can be imported
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Now we can import from base
from base.App import App
from base.ui.app import app
from base.tools.log import Log
from werkzeug.serving import run_simple

# Host name
hn = "127.0.0.1"

# Port Number
pt = 5000

# is flask working on debug mode
debug = False

if __name__ == "__main__":
    # Initialize the app (sets up database, etc.)
    App()

    # Start Flask server
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    url = f"http://{hn}:{pt}"
    Log.success(f"Flask UI running on {url}")
    run_simple(
        hostname=hn,
        port=pt,
        application=app,
        use_reloader=False,
        use_debugger=debug,
        threaded=True
    )