import unittest
import sqlite3
import sys
import os

# -----------------------------------------------------------------------
# Setup path to import project modules
# -----------------------------------------------------------------------
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))
sys.path.insert(0, project_root)

TEST_DB_NAME = "test_university_wellbeing.db"


class TestStudentCRUD(unittest.TestCase):

    def setUp(self):
        self.conn = sqlite3.connect(TEST_DB_NAME)
        self.cursor = self.conn.cursor()

        # Create full schema (students-only is enough for FR-003–005)
        self.cursor.executescript("""
            PRAGMA foreign_keys = ON;

            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                personal_tutor_email TEXT NOT NULL,
                emergency_contact_name TEXT, 
                emergency_contact_phone TEXT
            );
        """)

        self.conn.commit()

    def tearDown(self):
        self.conn.close()
        if os.path.exists(TEST_DB_NAME):
            os.remove(TEST_DB_NAME)

    # ==========================================
    # FR-003: Add New Student
    # ==========================================

    def test_insert_student_success(self):
        # Test that a new student record can be successfully inserted.
        self.cursor.execute("""
            INSERT INTO students 
            (student_id, first_name, last_name, email, personal_tutor_email,
             emergency_contact_name, emergency_contact_phone)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (1, "Alice", "Brown", "alice@uni.com", "tutor@uni.com", "Mom", "07123456789"))

        self.conn.commit()

        self.cursor.execute("SELECT * FROM students WHERE student_id = 1")
        student = self.cursor.fetchone()

        self.assertIsNotNone(student, "Student record should exist after insertion")
        self.assertEqual(student[1], "Alice", "First name should match")

    # ==========================================
    # FR-004: Update Existing Student
    # ==========================================

    def test_update_student_success(self):
        # Test that an existing student's information can be updated.
        # Insert test student
        self.cursor.execute("""
            INSERT INTO students 
            VALUES (1, 'Alice', 'Brown', 'alice@uni.com', 'tutor@uni.com', 'Mother', '07123456789')
        """)

        # Update operation
        self.cursor.execute("""
            UPDATE students
            SET first_name = ?, last_name = ?
            WHERE student_id = ?
        """, ("Alicia", "Green", 1))

        self.conn.commit()

        # Verify update
        self.cursor.execute("SELECT first_name, last_name FROM students WHERE student_id = 1")
        updated = self.cursor.fetchone()

        self.assertEqual(updated[0], "Alicia", "Updated first name should persist")
        self.assertEqual(updated[1], "Green", "Updated last name should persist")

    # ==========================================
    # FR-005: Delete Student
    # ==========================================

    def test_delete_student_success(self):
        # Test that a student record can be deleted.
        # Insert test student
        self.cursor.execute("""
            INSERT INTO students 
            VALUES (1, 'John', 'Smith', 'john@uni.com', 'tutor@uni.com', 'Dad', '07999999999')
        """)

        # Delete operation
        self.cursor.execute("DELETE FROM students WHERE student_id = 1")
        self.conn.commit()

        # Verify deletion
        self.cursor.execute("SELECT * FROM students WHERE student_id = 1")
        deleted = self.cursor.fetchone()

        self.assertIsNone(deleted, "Student record should be removed from database")


if __name__ == '__main__':
    unittest.main()
