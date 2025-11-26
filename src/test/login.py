import unittest
import sqlite3
import sys
import os

# -----------------------------------------------------------------------
# 1. Setup the path so Python can find 'src'
# -----------------------------------------------------------------------
# Get the absolute path of the current file (src/test/login.py)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go up two levels to find the project root (the folder containing 'src')
project_root = os.path.abspath(os.path.join(current_dir, '../../'))

# Add the project root to sys.path
sys.path.insert(0, project_root)

from src.base.services.Login import login_user