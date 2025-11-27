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

    # --- Survey Tests ---

    def test_insert_survey_valid(self):
        success = add_survey(TEST_DB_NAME, student_id=1, week=1, stress=3, sleep=7.5)
        self.assertTrue(success)

    def test_insert_survey_invalid_stress(self):
        """Test inserting stress level 10 raises error."""
        with self.assertRaises(sqlite3.IntegrityError):
            add_survey(TEST_DB_NAME, 1, 1, stress=10, sleep=8)

    def test_retrieve_student_history_trends(self):
        add_survey(TEST_DB_NAME, 1, week=1, stress=2, sleep=8)
        add_survey(TEST_DB_NAME, 1, week=2, stress=4, sleep=6)
        add_survey(TEST_DB_NAME, 1, week=3, stress=5, sleep=4)

        history = get_student_history(TEST_DB_NAME, student_id=1)

        self.assertEqual(len(history), 3)
        if len(history) > 0:
            self.assertEqual(history[0]['week_number'], 1)
            self.assertEqual(history[2]['stress_level'], 5)

    # --- Analytics Tests ---

    def test_aggregated_wellbeing_metrics(self):
        """Test calculating average stress for a specific week."""
        # Student 1: High Stress (5)
        add_survey(TEST_DB_NAME, 1, week=1, stress=5, sleep=4)
        # Student 2: Low Stress (1)
        add_survey(TEST_DB_NAME, 2, week=1, stress=1, sleep=9)

        # Average stress should be 3.0
        avg_stress = get_aggregated_stress_level(TEST_DB_NAME, week=1)
        self.assertEqual(avg_stress, 3.0)

if __name__ == '__main__':
    unittest.main()