import unittest
import sys
import os
import sqlite3

CURRENT_DIR = os.path.dirname(__file__)
SRC_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..","..",".."))
sys.path.insert(0, SRC_PATH)

from test.base_test.repository_test.student_repo_test import Student_Repo_test
from test.base_test.entity_test.student_test import Student_test
from test.base_test.repository_test.base_repo_test import Base_Repo_test

TEST_DB = "test_student_repo.db"


class TestStudentRepo(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB):
            try:
                os.remove(TEST_DB)
            except:
                pass

        Base_Repo_test.set_db_path_test(TEST_DB)

        self.repo = Student_Repo_test()
        self.repo.conn.row_factory = sqlite3.Row
        self.repo.cursor = self.repo.conn.cursor()

        self.conn = sqlite3.connect(TEST_DB)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE students (
                student_id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                email TEXT,
                personal_tutor_email TEXT,
                emergency_contact_name TEXT,
                emergency_contact_phone TEXT
            )
        """)

        self.cursor.execute("""
            INSERT INTO students
            (student_id, first_name, last_name, email,
            personal_tutor_email, emergency_contact_name, emergency_contact_phone)
            VALUES (1, 'Alice', 'Brown', 'alice@uni.com',
                    'tutor@uni.com', 'Dad', '07999999999')
        """)
        self.conn.commit()

    def tearDown(self):
        try: self.repo.conn.close()
        except: pass
        try: self.conn.close()
        except: pass
        try: os.remove(TEST_DB)
        except: pass

    # Test fetching a student by ID.
    def test_getStudent(self):
        s = self.repo.getStudent(1)
        self.assertIsNotNone(s)
        self.assertEqual(s.id, 1)
        self.assertEqual(s.first_name, 'Alice')
        self.assertEqual(s.last_name, 'Brown')

    # Test fetching a non-existing student returns None.
    def test_getStudent_not_found(self):
        s = self.repo.getStudent(999)
        self.assertIsNone(s)

    # Test fetching all students returns list of correct length.
    def test_getAllStudent(self):
        students = self.repo.getAllStudent()
        self.assertEqual(len(students), 1)
        self.assertEqual(students[0].id, 1)

    # Test adding a new student to the table.
    def test_addStudent(self):
        new_s = Student_test(
            id=2,
            first_name="Bob",
            last_name="Lee",
            email="bob@mail.com",
            personal_tutor_email="tutor2@mail.com",
            emergency_contact_name="Dad",
            emergency_contact_phone="222222"
        )

        result_id = self.repo.addStudent(new_s)
        self.assertEqual(result_id, 2)

        self.cursor.execute("SELECT * FROM students WHERE student_id = 2")
        row = self.cursor.fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row["first_name"], "Bob")

    # Test error is raised when required fields are missing.
    def test_addStudent_missing_fields(self):
        incomplete = Student_test(
            id=3,
            first_name="",
            last_name="Lee",
            email="",
            personal_tutor_email="tutor@mail.com",
            emergency_contact_name="Dad",
            emergency_contact_phone="333333"
        )

        with self.assertRaises(ValueError):
            self.repo.addStudent(incomplete)

    # Test updating an existing student's information.
    def test_updateStudent(self):
        update_data = Student_test(
            id=1,
            first_name="AliceUpdated",
            last_name=None,
            email="alice_new@mail.com",
            personal_tutor_email=None,
            emergency_contact_name=None,
            emergency_contact_phone=None
        )

        success = self.repo.updateStudent(update_data)
        self.assertTrue(success)

        self.cursor.execute("SELECT * FROM students WHERE student_id = 1")
        row = self.cursor.fetchone()
        self.assertEqual(row["first_name"], "AliceUpdated")
        self.assertEqual(row["email"], "alice_new@mail.com")

    # Test deleting a student by ID.
    def test_deleteStudent(self):
        to_delete = Student_test(
            id=1,
            first_name="Alice",
            last_name="Brown",
            email="alice@uni.com",
            personal_tutor_email="tutor@uni.com",
            emergency_contact_name="Dad",
            emergency_contact_phone="07999999999"
        )

        result = self.repo.deleteStudent(to_delete)
        self.assertTrue(result)

        self.cursor.execute("SELECT * FROM students WHERE student_id = 1")
        self.assertIsNone(self.cursor.fetchone())

    # Test delete returns False when student does not exist.
    def test_deleteStudent_not_found(self):
        fake_student = Student_test(
            id=999,
            first_name="Ghost",
            last_name="User",
            email=""
        )

        result = self.repo.deleteStudent(fake_student)
        self.assertFalse(result)

    # Test converting a DB row to Student object.
    def test_toStudent(self):
        self.cursor.execute("SELECT * FROM students WHERE student_id = 1")
        row = self.cursor.fetchone()

        obj = self.repo.toStudent(row)
        self.assertIsInstance(obj, Student_test)
        self.assertEqual(obj.id, 1)

    # Test converting multiple rows to Student objects.
    def test_toStudents(self):
        self.cursor.execute("SELECT * FROM students")
        rows = self.cursor.fetchall()

        students = self.repo.toStudents(rows)
        self.assertEqual(len(students), 1)
        self.assertIsInstance(students[0], Student_test)


if __name__ == "__main__":
    unittest.main()
