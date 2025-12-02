import unittest
import sqlite3
import sys
import os

CURRENT_DIR = os.path.dirname(__file__)
SRC_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", "..",".." ))
sys.path.insert(0, SRC_PATH)

# ========= CORRECT IMPORTS (MATCH YOUR PROJECT STRUCTURE) ==========
from test.base_test.repository_test.base_repo_test import Base_Repo_test
from test.base_test.services_test.student_service_test import Student_Service_test

from test.base_test.entity_test.student_test import Student_test
from test.base_test.entity_test.attendance_test import Attendance_test
from test.base_test.entity_test.assessments_test import Assessment_test
from test.base_test.entity_test.wellbeing_survey_test import Wellbeing_Survey_test


TEST_DB = "test_student_service.db"


class TestStudentService(unittest.TestCase):

    def setUp(self):

        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

        # Give the DB path to Base_Repo_test
        Base_Repo_test.set_db_path_test(TEST_DB)

        # Open DB manually
        self.conn = sqlite3.connect(TEST_DB)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

        # Create all required tables
        self.cursor.executescript("""
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

        # Insert sample test data
        self.cursor.execute("""
            INSERT INTO students VALUES
            (1, 'Alice', 'Brown', 'alice@mail.com', 'tutor@mail.com', 'Dad', '123456')
        """)

        self.cursor.execute("""
            INSERT INTO attendance VALUES
            (1, 1, 3, 1, 0)
        """)

        self.cursor.execute("""
            INSERT INTO assessments VALUES
            (1, 1, 'Assignment A', 85, '2024-10-01')
        """)

        self.cursor.execute("""
            INSERT INTO wellbeing_surveys VALUES
            (1, 1, 3, 7, 6.5, '2024-12-01')
        """)

        self.conn.commit()

        self.service = Student_Service_test()

    def tearDown(self):
        try:
            self.conn.close()
        except:
            pass

        if os.path.exists(TEST_DB):
            try:
                os.remove(TEST_DB)
            except:
                pass

    # ============================================================
    # =============== TEST CASES =================================
    # ============================================================

    def test_getAllStudent(self):
        students = self.service.getAllStudent()
        self.assertEqual(len(students), 1)
        self.assertEqual(students[0].first_name, "Alice")

    def test_getAttendanceByID(self):
        att = self.service.getAttdenceByID(1)
        self.assertEqual(len(att), 1)
        self.assertIsInstance(att[0], Attendance_test)

    def test_getAssessmentByID(self):
        assessments = self.service.getAssessmentByID(1)
        self.assertEqual(len(assessments), 1)
        self.assertIsInstance(assessments[0], Assessment_test)

    def test_getWellBeingSurveyByID(self):
        surveys = self.service.getWellBeingSurveyByID(1)
        self.assertEqual(len(surveys), 1)
        self.assertIsInstance(surveys[0], Wellbeing_Survey_test)

    def test_add_update_delete_student(self):
        # ADD
        new_student = Student_test(
            id=2,
            name="Test",
            gender="F",
            first_name="Anna",
            last_name="Lee",
            email="annalee@mail.com",
            personal_tutor_email="tutor@mail.com",
            emergency_contact_name="Mom",
            emergency_contact_phone="654321"
        )

        self.service.add(new_student)

        self.cursor.execute("SELECT * FROM students WHERE student_id = 2")
        added = self.cursor.fetchone()
        self.assertIsNotNone(added)

        # UPDATE
        new_student.first_name = "Updated"
        self.service.update(new_student)

        self.cursor.execute("SELECT * FROM students WHERE student_id = 2")
        updated = self.cursor.fetchone()
        self.assertEqual(updated["first_name"], "Updated")

        # DELETE
        self.service.delete(new_student)

        self.cursor.execute("SELECT * FROM students WHERE student_id = 2")
        deleted = self.cursor.fetchone()
        self.assertIsNone(deleted)


if __name__ == "__main__":
    unittest.main()
