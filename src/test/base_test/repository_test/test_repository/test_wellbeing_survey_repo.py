import unittest
import sys
import os

CURRENT_DIR = os.path.dirname(__file__)

SRC_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..",".."))
sys.path.insert(0, SRC_PATH)
import sqlite3

# ===========================================================================
# PLACEHOLDERS (STUBS)
# ===========================================================================

from repository_test.wellbeing_survey_repo_test import Wellbeing_Survey_Repo_test
from entity_test.wellbeing_survey_test import Wellbeing_Survey_test
from repository_test.base_repo_test import Base_Repo_test

TEST_DB = "test_wellbeing_survey_repo.db"

def setup_test_db():
    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE wellbeing_surveys (
            survey_id INTEGER PRIMARY KEY,
            student_id INTEGER,
            week_number INTEGER,
            stress_level INTEGER,
            hours_slept REAL,
            survey_date TEXT
        );
    """)
    conn.commit()
    return conn, cursor

# ===========================================================================
# END PLACEHOLDERS
# ===========================================================================


class TestWellbeingSurveyRepo(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

        self.conn, self.cursor = setup_test_db()
        Base_Repo_test.set_db_path_test(TEST_DB)
        self.repo = Wellbeing_Survey_Repo_test()

        # Insert initial test survey
        self.cursor.execute("""
            INSERT INTO wellbeing_surveys
            (survey_id, student_id, week_number, stress_level, hours_slept, survey_date)
            VALUES (1, 10, 1, 3, 7.5, '2025-01-01')
        """)
        self.conn.commit()

    def tearDown(self):
        self.conn.close()
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_getWellBeingSurvey_test(self):
        """Test fetching a wellbeing survey by ID."""
        s = self.repo.getWellBeingSurvey_test(1)

        self.assertIsNotNone(s)
        self.assertEqual(s.survey_id_test, 1)
        self.assertEqual(s.student_id_test, 10)
        self.assertEqual(s.week_number_test, 1)
        self.assertEqual(s.stress_level_test, 3)

    def test_getWellBeingSurvey_test_not_found(self):
        """Test fetching a non-existing survey returns None."""
        s = self.repo.getWellBeingSurvey_test(999)
        self.assertIsNone(s)

    def test_getWellBeingSurveys_test(self):
        """Test fetching all surveys returns correct list."""
        surveys = self.repo.getWellBeingSurveys_test()

        self.assertEqual(len(surveys), 1)
        self.assertEqual(surveys[0].survey_id_test, 1)

    def test_getWellBeingSurveysByStudentID_test(self):
        """Test fetching surveys by student ID."""
        # Insert additional entry
        self.cursor.execute("""
            INSERT INTO wellbeing_surveys
            (survey_id, student_id, week_number, stress_level, hours_slept, survey_date)
            VALUES (2, 10, 2, 4, 6, '2025-01-02')
        """)
        self.conn.commit()

        surveys = self.repo.getWellBeingSurveysByStudentID_test(10)

        self.assertEqual(len(surveys), 2)
        self.assertEqual(surveys[0].student_id_test, 10)
        self.assertEqual(surveys[1].student_id_test, 10)

    def test_toWellBeingSurvey_test(self):
        """Test converting a DB row into Wellbeing_Survey_test object."""
        self.cursor.execute("SELECT * FROM wellbeing_surveys WHERE survey_id = 1")
        row = self.cursor.fetchone()

        survey = self.repo.toWellBeingSurvey_test(row)

        self.assertIsInstance(survey, Wellbeing_Survey_test)
        self.assertEqual(survey.survey_id_test, 1)

    def test_toWellBeingSurveys_test(self):
        """Test converting multiple DB rows into Wellbeing_Survey_test objects."""
        self.cursor.execute("SELECT * FROM wellbeing_surveys")
        rows = self.cursor.fetchall()

        surveys = self.repo.toWellBeingSurveys_test(rows)

        self.assertEqual(len(surveys), 1)
        self.assertIsInstance(surveys[0], Wellbeing_Survey_test)


if __name__ == "__main__":
    unittest.main()
