import unittest
import sqlite3
import sys
import os

CURRENT_DIR = os.path.dirname(__file__)
SRC_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", ".." ,".."))
sys.path.insert(0, SRC_PATH)

from test.base_test.repository_test.assessment_repo_test import Assessment_Repo_test
from test.base_test.entity_test.assessments_test import Assessment_test
from test.base_test.repository_test.base_repo_test import Base_Repo_test


TEST_DB = "test_assessments_repo.db"


def setup_test_db():
    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE assessments (
            assessment_id INTEGER PRIMARY KEY,
            student_id INTEGER,
            assignment_name TEXT,
            grade INTEGER,
            submitted_on_time TEXT
        );
    """)
    conn.commit()
    return conn, cursor


class TestAssessmentRepo(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

        self.conn, self.cursor = setup_test_db()
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

        Base_Repo_test.set_db_path_test(TEST_DB)
        self.repo = Assessment_Repo_test()

        self.repo.conn.row_factory = sqlite3.Row
        self.repo.cursor = self.repo.conn.cursor()

        self.cursor.execute("""
            INSERT INTO assessments
            (assessment_id, student_id, assignment_name, grade, submitted_on_time)
            VALUES (1, 10, 'Homework 1', 85, '2025-01-02')
        """)
        self.conn.commit()


    def tearDown(self):
        try:
            self.repo.conn.close()
        except:
            pass

        del self.repo

        try:
            self.conn.close()
        except:
            pass

        if os.path.exists(TEST_DB):
            try:
                os.remove(TEST_DB)
            except:
                pass

    def test_getAssessment(self):
        """Test fetching a single assessment by ID."""
        a = self.repo.getAssessment(1)
        self.assertIsNotNone(a)
        self.assertEqual(a.assessment_id, 1)
        self.assertEqual(a.student_id, 10)
        self.assertEqual(a.assignment_name, "Homework 1")
        self.assertEqual(a.grade, 85)

    def test_getAssessment_not_found(self):
        """Test fetching an ID that does not exist returns None."""
        a = self.repo.getAssessment(999)
        self.assertIsNone(a)

    def test_getAssessments(self):
        """Test fetching all assessments returns list with correct items."""
        items = self.repo.getAssessments()
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].assessment_id, 1)

    def test_getAssessmentsByStudentID(self):
        """Test fetching assessments for a specific student."""
        self.cursor.execute("""
            INSERT INTO assessments
            (assessment_id, student_id, assignment_name, grade, submitted_on_time)
            VALUES (2, 10, 'Quiz', 92, '2025-01-03')
        """)
        self.conn.commit()

        res = self.repo.getAssessmentsByStudentID(10)

        # repo behavior: returns Assessment_test, not list
        self.assertIsInstance(res, Assessment_test)
        self.assertEqual(res.student_id, 10)

    def test_toAssessment(self):
        """Test converting a DB row into Assessment_test object."""
        self.cursor.execute("SELECT * FROM assessments WHERE assessment_id = 1")
        row = self.cursor.fetchone()
        obj = self.repo.toAssessment(row)
        self.assertIsInstance(obj, Assessment_test)
        self.assertEqual(obj.assessment_id, 1)

    def test_toAssessments(self):
        """Test converting multiple DB rows into list of Assessment_test."""
        self.cursor.execute("SELECT * FROM assessments")
        rows = self.cursor.fetchall()

        result = self.repo.toAssessments(rows)

        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], Assessment_test)


if __name__ == "__main__":
    unittest.main()
