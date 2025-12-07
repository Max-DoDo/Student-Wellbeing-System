import unittest
import os
import sqlite3

# ===========================================================================
# PLACEHOLDERS (STUBS)
# ===========================================================================

from repository_test.student_repo_test import Student_Repo_test
from entity_test.student_test import Student_test
from repository_test.base_repo_test import Base_Repo_test

TEST_DB = "test_student_repo.db"

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
    """)
    conn.commit()
    return conn, cursor

# ===========================================================================
# END PLACEHOLDERS
# ===========================================================================


class TestStudentRepo(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

        self.conn, self.cursor = setup_test_db()
        Base_Repo_test.set_db_path_test(TEST_DB)
        self.repo = Student_Repo_test()

        # Insert initial student
        self.cursor.execute("""
            INSERT INTO students
            (student_id, first_name, last_name, email, personal_tutor_email, emergency_contact_name, emergency_contact_phone)
            VALUES (1, 'Alice', 'Smith', 'alice@mail.com', 'tutor@mail.com', 'Mom', '111111')
        """)
        self.conn.commit()

    def tearDown(self):
        self.conn.close()
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_getStudent_test(self):
        """Test fetching a student by ID."""
        s = self.repo.getStudent_test(1)

        self.assertIsNotNone(s)
        self.assertEqual(s.id_test, 1)
        self.assertEqual(s.first_name_test, 'Alice')
        self.assertEqual(s.last_name_test, 'Smith')

    def test_getStudent_test_not_found(self):
        """Test fetching a non-existing student returns None."""
        s = self.repo.getStudent_test(999)
        self.assertIsNone(s)

    def test_getAllStudent_test(self):
        """Test fetching all students returns list of correct length."""
        students = self.repo.getAllStudent_test()

        self.assertEqual(len(students), 1)
        self.assertEqual(students[0].id_test, 1)

    def test_addStudent_test(self):
        """Test adding a new student to the table."""
        new_s = Student_test(
            id_test=2,
            first_name_test="Bob",
            last_name_test="Lee",
            email_test="bob@mail.com",
            personal_tutor_email_test="tutor2@mail.com",
            emergency_contact_name_test="Dad",
            emergency_contact_phone_test="222222"
        )

        result_id = self.repo.addStudent_test(new_s)

        self.assertEqual(result_id, 2)

        self.cursor.execute("SELECT * FROM students WHERE student_id = 2")
        row = self.cursor.fetchone()

        self.assertIsNotNone(row)
        self.assertEqual(row["first_name"], "Bob")

    def test_addStudent_test_missing_fields(self):
        """Test error is raised when required fields are missing."""
        incomplete = Student_test(
            id_test=3,
            first_name_test="",
            last_name_test="Lee",
            email_test="",
            personal_tutor_email_test="tutor@mail.com",
            emergency_contact_name_test="Dad",
            emergency_contact_phone_test="333333"
        )

        with self.assertRaises(ValueError):
            self.repo.addStudent_test(incomplete)

    def test_updateStudent_test(self):
        """Test updating an existing student's information."""
        update_data = Student_test(
            id_test=1,
            first_name_test="AliceUpdated",
            last_name_test=None,
            email_test="alice_new@mail.com",
            personal_tutor_email_test=None,
            emergency_contact_name_test=None,
            emergency_contact_phone_test=None
        )

        success = self.repo.updateStudent_test(update_data)
        self.assertTrue(success)

        self.cursor.execute("SELECT * FROM students WHERE student_id = 1")
        row = self.cursor.fetchone()

        self.assertEqual(row["first_name"], "AliceUpdated")
        self.assertEqual(row["email"], "alice_new@mail.com")

    def test_deleteStudent_test(self):
        """Test deleting a student by ID."""
        to_delete = Student_test(
            id_test=1,
            first_name_test="Alice",
            last_name_test="Smith",
            email_test="alice@mail.com",
            personal_tutor_email_test="tutor@mail.com",
            emergency_contact_name_test="Mom",
            emergency_contact_phone_test="111111"
        )

        result = self.repo.deleteStudent_test(to_delete)
        self.assertTrue(result)

        self.cursor.execute("SELECT * FROM students WHERE student_id = 1")
        self.assertIsNone(self.cursor.fetchone())

    def test_deleteStudent_test_not_found(self):
        """Test delete returns False when student does not exist."""
        fake_student = Student_test(
            id_test=999,
            first_name_test="Ghost",
            last_name_test="User",
            email_test="",
        )

        result = self.repo.deleteStudent_test(fake_student)
        self.assertFalse(result)

    def test_toStudent_test(self):
        """Test converting a DB row to Student_test object."""
        self.cursor.execute("SELECT * FROM students WHERE student_id = 1")
        row = self.cursor.fetchone()

        obj = self.repo.toStudent_test(row)

        self.assertIsInstance(obj, Student_test)
        self.assertEqual(obj.id_test, 1)

    def test_toStudents_test(self):
        """Test converting multiple rows to Student_test objects."""
        self.cursor.execute("SELECT * FROM students")
        rows = self.cursor.fetchall()

        students = self.repo.toStudents_test(rows)

        self.assertEqual(len(students), 1)
        self.assertIsInstance(students[0], Student_test)


if __name__ == "__main__":
    unittest.main()
