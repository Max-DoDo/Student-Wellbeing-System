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

TEST_DB_NAME = "test_wellbeing.db"

class TestWellbeingFeatures(unittest.TestCase):

    def setUp(self):
        self.conn = sqlite3.connect(TEST_DB_NAME)
        self.cursor = self.conn.cursor()
        
        self.cursor.executescript("""
            CREATE TABLE students (student_id INTEGER PRIMARY KEY);
            CREATE TABLE wellbeing_surveys (
                survey_id INTEGER PRIMARY KEY, student_id INTEGER, 
                week_number INTEGER, 
                stress_level INTEGER CHECK(stress_level BETWEEN 1 AND 5), 
                hours_slept REAL
            );
        """)
        self.cursor.execute("INSERT INTO students (student_id) VALUES (1)")
        self.cursor.execute("INSERT INTO students (student_id) VALUES (2)")
        self.conn.commit()

    def tearDown(self):
        self.conn.close()
        if os.path.exists(TEST_DB_NAME):
            os.remove(TEST_DB_NAME)

if __name__ == '__main__':
    unittest.main()