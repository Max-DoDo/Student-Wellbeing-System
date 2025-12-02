import unittest
import os
import sqlite3

# ===========================================================================
# PLACEHOLDERS (STUBS)
# ===========================================================================

from repository_test.assessment_repo_test import Assessment_Repo_test
from entity_test.assessments_test import Assessment_test
from repository_test.base_repo_test import Base_Repo_test

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

# ===========================================================================
# END PLACEHOLDERS
# ===========================================================================


class TestAssessmentRepo(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

        self.conn, self.cursor = setup_test_db()
        Base_Repo_test.DB_PATH = TEST_DB
        self.repo = Assessment_Repo_test()

        # Insert sample data
        self.cursor.execute("""
            INSERT INTO assessments
            (assessment_id, student_id, assignment_name, grade, submitted_on_time)
            VALUES (1, 10, 'Homework 1', 85, '2025-01-02')
        """)
        self.conn.commit()

    def tearDown(self):
        self.conn.close()
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_getAssessment(self):
        """Test fetching a single assessment by ID."""
        a = self.repo.getAssessment(1)

        self.assertIsNotNone(a)
        self.assertEqual(a.assessment_id_test, 1)
        self.assertEqual(a.student_id_test, 10)
        self.assertEqual(a.assignment_name_test, "Homework 1")
        self.assertEqual(a.grade_test, 85)

    def test_getAssessment_not_found(self):
        """Test fetching an ID that does not exist returns None."""
        a = self.repo.getAssessment(999)
        self.assertIsNone(a)

    def test_getAssessments(self):
        """Test fetching all assessments returns list with correct items."""
        items = self.repo.getAssessments()

        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].assessment_id_test, 1)

    def test_getAssessmentsByStudentID(self):
        """Test fetching assessments for a specific student."""
        # Insert another
        self.cursor.execute("""
            INSERT INTO assessments
            (assessment_id, student_id, assignment_name, grade, submitted_on_time)
            VALUES (2, 10, 'Quiz', 92, '2025-01-03')
        """)
        self.conn.commit()

        items = self.repo.getAssessmentsByStudentID(10)

        # expected 2 rows
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0].student_id_test, 10)
        self.assertEqual(items[1].student_id_test, 10)

    def test_toAssessment(self):
        """Test toAssessment converts a DB row into Assessment_test object."""
        self.cursor.execute("SELECT * FROM assessments WHERE assessment_id = 1")
        row = self.cursor.fetchone()

        obj = self.repo.toAssessment(row)

        self.assertIsInstance(obj, Assessment_test)
        self.assertEqual(obj.assessment_id_test, 1)

    def test_toAssessments(self):
        """Test converting multiple DB rows into Assessment_test list."""
        self.cursor.execute("SELECT * FROM assessments")
        rows = self.cursor.fetchall()

        result = self.repo.toAssessments(rows)

        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], Assessment_test)


if __name__ == '__main__':
    unittest.main()
