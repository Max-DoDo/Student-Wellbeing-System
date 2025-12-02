import unittest
import sys
import os
import sqlite3

CURRENT_DIR = os.path.dirname(__file__)
SRC_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", "..", ".."))
sys.path.insert(0, SRC_PATH)

from test.base_test.repository_test.wellbeing_survey_repo_test import Wellbeing_Survey_Repo_test
from test.base_test.entity_test.wellbeing_survey_test import Wellbeing_Survey_test
from test.base_test.repository_test.base_repo_test import Base_Repo_test

TEST_DB = "test_wellbeing_survey_repo.db"


class TestWellbeingSurveyRepo(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

        Base_Repo_test.set_db_path_test(TEST_DB)

        self.repo = Wellbeing_Survey_Repo_test()
        self.repo.conn.row_factory = sqlite3.Row
        self.cursor = self.repo.conn.cursor()
        self.repo.cursor = self.cursor

        # Create table
        self.cursor.executescript("""
            CREATE TABLE wellbeing_surveys (
                survey_id INTEGER PRIMARY KEY,
                student_id INTEGER,
                week_number INTEGER,
                stress_level INTEGER,
                hours_slept REAL,
                survey_date TEXT
            );
        """)

        # Insert initial row
        self.cursor.execute("""
            INSERT INTO wellbeing_surveys
            (survey_id, student_id, week_number, stress_level, hours_slept, survey_date)
            VALUES (1, 10, 3, 7, 6.5, '2024-12-01')
        """)

        self.repo.conn.commit()

    def tearDown(self):
        try:
            self.repo.conn.close()
        except:
            pass

        if os.path.exists(TEST_DB):
            try:
                os.remove(TEST_DB)
            except:
                pass

    # =====================================================
    # TESTS START HERE
    # =====================================================

    def test_getWellBeingSurvey(self):
        s = self.repo.getWellBeingSurvey(1)

        self.assertIsNotNone(s)
        self.assertEqual(s.survey_id, 1)
        self.assertEqual(s.student_id, 10)
        self.assertEqual(s.week_number, 3)
        self.assertEqual(s.stress_level, 7)

    def test_getWellBeingSurvey_not_found(self):
        s = self.repo.getWellBeingSurvey(999)
        self.assertIsNone(s)

    def test_getWellBeingSurveys(self):
        surveys = self.repo.getWellBeingSurveys()

        self.assertEqual(len(surveys), 1)
        self.assertEqual(surveys[0].survey_id, 1)

    def test_getWellBeingSurveysByStudentID(self):
        # Insert second row
        self.cursor.execute("""
            INSERT INTO wellbeing_surveys
            (survey_id, student_id, week_number, stress_level, hours_slept, survey_date)
            VALUES (2, 10, 2, 4, 5, '2025-01-02')
        """)
        self.repo.conn.commit()

        surveys = self.repo.getWellBeingSurveysByStudentID(10)

        self.assertEqual(len(surveys), 2)
        self.assertEqual(surveys[0].student_id, 10)
        self.assertEqual(surveys[1].student_id, 10)

    def test_toWellBeingSurvey(self):
        self.cursor.execute("SELECT * FROM wellbeing_surveys WHERE survey_id = 1")
        row = self.cursor.fetchone()

        survey = self.repo.toWellBeingSurvey(row)

        self.assertIsInstance(survey, Wellbeing_Survey_test)
        self.assertEqual(survey.survey_id, 1)

    def test_toWellBeingSurveys(self):
        self.cursor.execute("SELECT * FROM wellbeing_surveys")
        rows = self.cursor.fetchall()

        surveys = self.repo.toWellBeingSurveys(rows)

        self.assertEqual(len(surveys), 1)
        self.assertIsInstance(surveys[0], Wellbeing_Survey_test)


if __name__ == "__main__":
    unittest.main()

