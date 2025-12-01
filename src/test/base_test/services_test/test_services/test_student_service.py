import unittest
import sys
import os

CURRENT_DIR = os.path.dirname(__file__)

SRC_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".." ))
sys.path.insert(0, SRC_PATH)
import sqlite3

# ===========================================================================
# PLACEHOLDERS (STUBS)
# ===========================================================================

from services_test.student_service_test import Student_Service_test
from repository_test.base_repo_test import Base_Repo_test
from entity_test.student_test import Student_test
from entity_test.attendance_test import Attendance_test
from entity_test.assessments_test import Assessment_test
from entity_test.wellbeing_survey_test import Wellbeing_Survey_test

TEST_DB = "test_student_service.db"

def setup_test_db():
    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE students (
            student_id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            personal_tutor_email TEXT,
            emergency_contact_name TEXT,
            emergency_contact_phone TEXT
        );

        CREATE TABLE attendance (
            attendance_id INTEGER PRIMARY KEY,
            student_id INTEGER,
            week_number INTEGER,
            is_present INTEGER,
            is_late INTEGER
        );

        CREATE TABLE assessments (
            assessment_id INTEGER PRIMARY KEY,
            student_id INTEGER,
            assignment_name TEXT,
            grade INTEGER,
            submitted_on_time TEXT
        );

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


class TestStudentService(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

        self.conn, self.cursor = setup_test_db()
        Base_Repo_test.set_db_path_test(TEST_DB)

        # Insert baseline student
        self.cursor.execute("""
            INSERT INTO students
            (student_id, first_name, last_name, email)
            VALUES (1, 'Alice', 'Smith', 'alice@mail.com')
        """)

        # Insert related attendance
        self.cursor.execute("""
            INSERT INTO attendance
            (attendance_id, student_id, week_number, is_present, is_late)
            VALUES (1, 1, 1, 1, 0)
        """)

        # Insert related assessment
        self.cursor.execute("""
            INSERT INTO assessments
            (assessment_id, student_id, assignment_name, grade, submitted_on_time)
            VALUES (1, 1, 'Assignment 1', 85, '2025-01-01')
        """)

        # Insert related wellbeing survey
        self.cursor.execute("""
            INSERT INTO wellbeing_surveys
            (survey_id, student_id, week_number, stress_level, hours_slept, survey_date)
            VALUES (1, 1, 1, 3, 7.5, '2025-01-01')
        """)

        self.conn.commit()

        self.service = Student_Service_test()

    def tearDown(self):
        self.conn.close()
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_getAllStudent_test(self):
        """Test retrieving all students."""
        result = self.service.getAllStudent_test()

        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], Student_test)
        self.assertEqual(result[0].id_test, 1)

    def test_getAttdenceByID_test(self):
        """Test retrieving all attendance for a student."""
        result = self.service.getAttdenceByID_test(1)

        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], Attendance_test)
        self.assertEqual(result[0].student_id_test, 1)

    def test_getAssessmentByID_test(self):
        """Test retrieving student assessments."""
        result = self.service.getAssessmentByID_test(1)

        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], Assessment_test)
        self.assertEqual(result[0].assignment_name_test, "Assignment 1")

    def test_getWellBeingSurveyByID_test(self):
        """Test retrieving wellbeing surveys for a student."""
        result = self.service.getWellBeingSurveyByID_test(1)

        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], Wellbeing_Survey_test)
        self.assertEqual(result[0].week_number_test, 1)

    def test_add_test(self):
        """Test calling add_test triggers repo insert logic."""
        new_student = Student_test(
            id_test=2,
            first_name_test="Bob",
            last_name_test="Jones",
            email_test="bob@mail.com"
        )

        # Should not raise errors since repo_test uses real SQL insert
        self.service.add_test(new_student)

        self.cursor.execute("SELECT * FROM students WHERE student_id = 2")
        row = self.cursor.fetchone()

        self.assertIsNotNone(row)
        self.assertEqual(row["first_name"], "Bob")

    def test_delete_test(self):
        """Test deleting an existing student."""
        student = Student_test(id_test=1)

        self.service.delete_test(student)

        self.cursor.execute("SELECT * FROM students WHERE student_id = 1")
        row = self.cursor.fetchone()

        self.assertIsNone(row)

if __name__ == "__main__":
    unittest.main()
