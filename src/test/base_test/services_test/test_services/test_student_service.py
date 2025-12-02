import unittest
import sqlite3
import sys
import os
import gc

CURRENT_DIR = os.path.dirname(__file__)
SRC_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", "..",".." ))
sys.path.insert(0, SRC_PATH)

from test.base_test.repository_test.base_repo_test import Base_Repo_test
from test.base_test.services_test.student_service_test import Student_Service_test

from test.base_test.repository_test.student_repo_test import Student_Repo_test
from test.base_test.repository_test.attendance_repo_test import Attendance_Repo_test
from test.base_test.repository_test.assessment_repo_test import Assessment_Repo_test
from test.base_test.repository_test.wellbeing_survey_repo_test import Wellbeing_Survey_Repo_test

from test.base_test.entity_test.student_test import Student_test
from test.base_test.entity_test.attendance_test import Attendance_test
from test.base_test.entity_test.assessments_test import Assessment_test
from test.base_test.entity_test.wellbeing_survey_test import Wellbeing_Survey_test


TEST_DB = "test_student_service.db"


class TestStudentService(unittest.TestCase):

    def setUp(self):
        gc.collect()

        try:
            sqlite3.connect(TEST_DB).close()
        except:
            pass

        if os.path.exists(TEST_DB):
            try:
                os.remove(TEST_DB)
            except:
                pass

        Base_Repo_test.set_db_path_test(TEST_DB)

        self.conn = sqlite3.connect(TEST_DB)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

        self.cursor.executescript("""
            DROP TABLE IF EXISTS students;
            DROP TABLE IF EXISTS attendance;
            DROP TABLE IF EXISTS assessments;
            DROP TABLE IF EXISTS wellbeing_surveys;

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

        self.cursor.execute("INSERT INTO students VALUES (1,'Alice','Brown','alice@mail.com','tutor@mail.com','Dad','123456')")
        self.cursor.execute("INSERT INTO attendance VALUES (1,1,3,1,0)")
        self.cursor.execute("INSERT INTO assessments VALUES (1,1,'Assignment A',85,'2024-10-01')")
        self.cursor.execute("INSERT INTO wellbeing_surveys VALUES (1,1,3,7,6.5,'2024-12-01')")
        self.conn.commit()

        self.repo_student = Student_Repo_test()
        self.repo_attendance = Attendance_Repo_test()
        self.repo_assessment = Assessment_Repo_test()
        self.repo_wellbeing = Wellbeing_Survey_Repo_test()

        self.service = Student_Service_test()
        self.service.student_repo = self.repo_student
        self.service.attendance_repo = self.repo_attendance
        self.service.assessment_repo = self.repo_assessment
        self.service.wellbeing_repo = self.repo_wellbeing


    def tearDown(self):
        gc.collect()
        try:
            self.conn.close()
        except:
            pass

        try:
            sqlite3.connect(TEST_DB).close()
        except:
            pass

        if os.path.exists(TEST_DB):
            try:
                os.remove(TEST_DB)
            except:
                pass


    def test_getAllStudent(self):
        s = self.service.student_repo.getAllStudent()
        self.assertEqual(len(s), 1)
        self.assertEqual(s[0].first_name, "Alice")

    def test_getAttendanceByID(self):
        a = self.service.attendance_repo.getAttendancesByStudentID(1)
        self.assertEqual(len(a), 1)
        self.assertIsInstance(a[0], Attendance_test)

    def test_getAssessmentByID(self):
        a = self.service.assessment_repo.getAssessmentsByStudentID(1)
        self.assertEqual(len(a), 1)
        self.assertIsInstance(a[0], Assessment_test)

    def test_getWellBeingSurveyByID(self):
        w = self.service.wellbeing_repo.getWellBeingSurveysByStudentID(1)
        self.assertEqual(len(w), 1)
        self.assertIsInstance(w[0], Wellbeing_Survey_test)

    def test_add_update_delete_student(self):
        s = Student_test(
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

        self.service.student_repo.addStudent(s)

        self.cursor.execute("SELECT * FROM students WHERE student_id = 2")
        added = self.cursor.fetchone()
        self.assertIsNotNone(added)

        s.first_name = "Updated"
        self.service.student_repo.updateStudent(s)

        self.cursor.execute("SELECT * FROM students WHERE student_id = 2")
        updated = self.cursor.fetchone()
        self.assertEqual(updated["first_name"], "Updated")

        self.service.student_repo.deleteStudent(s)

        self.cursor.execute("SELECT * FROM students WHERE student_id = 2")
        deleted = self.cursor.fetchone()
        self.assertIsNone(deleted)
    
    def test_service_getAllStudent(self):
        result = self.service.getAllStudent()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].first_name, "Alice")

    def test_service_getAttendanceByID(self):
        result = self.service.getAttdenceByID(1)
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], Attendance_test)

    def test_service_getAssessmentByID(self):
        try:
            result = self.service.getAssessmentByID(1)
        except:
            result = []
        self.assertEqual(len(result), 1)

    def test_service_getWellBeingSurveyByID(self):
        result = self.service.getWellBeingSurveyByID(1)
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], Wellbeing_Survey_test)

    def test_service_add_update_delete_student(self):
        s = Student_test(
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

        self.service.add(s)
        self.cursor.execute("SELECT * FROM students WHERE student_id = 2")
        added = self.cursor.fetchone()
        self.assertIsNotNone(added)

        s.first_name = "Updated"
        self.service.update(s)
        self.cursor.execute("SELECT * FROM students WHERE student_id = 2")
        updated = self.cursor.fetchone()
        self.assertEqual(updated["first_name"], "Updated")

        self.service.delete(s)
        self.cursor.execute("SELECT * FROM students WHERE student_id = 2")
        deleted = self.cursor.fetchone()
        self.assertIsNone(deleted)



if __name__ == "__main__":
    unittest.main()
