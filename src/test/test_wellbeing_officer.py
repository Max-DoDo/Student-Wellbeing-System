import unittest
import sqlite3
import os

# ===========================================================================
# PLACEHOLDERS (STUBS)
# ===========================================================================

def add_survey(db_name, student_id, week, stress, sleep):
    """Placeholder: Always fails"""
    return False

def get_student_history(db_name, student_id):
    """Placeholder: Returns empty list"""
    return []

def get_aggregated_stress_level(db_name, week):
    """Placeholder: Returns 0"""
    return 0.0

# ===========================================================================
# END PLACEHOLDERS
# ===========================================================================