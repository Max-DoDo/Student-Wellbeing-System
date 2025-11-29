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
    
    def test_insert_duplicate_student_id_fails(self):
        """Inserting the same student_id twice should raise an error."""
        self.cursor.execute("""
            INSERT INTO students VALUES
            (1, 'Alice', 'Brown', 'alice@uni.com',
             'tutor@uni.com', 'Mom', '07123456789')
        """)
        self.conn.commit()

        with self.assertRaises(sqlite3.IntegrityError):
            self.cursor.execute("""
                INSERT INTO students VALUES
                (1, 'Bob', 'Smith', 'bob@uni.com',
                 'tutor@uni.com', 'Dad', '07999999999')
            """)

    def test_insert_duplicate_email_fails(self):
        """Duplicate emails must be rejected (UNIQUE constraint)."""
        self.cursor.execute("""
            INSERT INTO students VALUES
            (1, 'Alice', 'Brown', 'dup@uni.com',
             'tutor@uni.com', 'Mom', '07123456789')
        """)
        self.conn.commit()

        with self.assertRaises(sqlite3.IntegrityError):
            self.cursor.execute("""
                INSERT INTO students VALUES
                (2, 'Mary', 'Smith', 'dup@uni.com',
                 'tutor@uni.com', 'Dad', '07999999999')
            """)

    def test_insert_missing_required_field_fails(self):
        """Missing NOT NULL fields should cause an insertion failure."""
        with self.assertRaises(sqlite3.IntegrityError):
            self.cursor.execute("""
                INSERT INTO students (student_id, first_name)
                VALUES (1, 'Alice')
            """)

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


    def test_update_student_duplicate_email_fails(self):
        # Existing students
        self.cursor.execute("""
            INSERT INTO students VALUES
            (1, 'Alice', 'Brown', 'alice@uni.com', 'tutor@uni.com', 'Mom', '07123456789')
        """)
        self.cursor.execute("""
            INSERT INTO students VALUES
            (2, 'Bob', 'Smith', 'bob@uni.com', 'tutor@uni.com', 'Dad', '07999999999')
        """)
        self.conn.commit()

        # Attempt to update student 1 to use Bob's email
        with self.assertRaises(sqlite3.IntegrityError):
            self.cursor.execute("""
                UPDATE students
                SET email = 'bob@uni.com'
                WHERE student_id = 1
            """)

    def test_update_nonexistent_student_no_error(self):
        # Update student who does NOT exist (student_id = 999)
        self.cursor.execute("""
            UPDATE students
            SET first_name = 'Ghost'
            WHERE student_id = 999
        """)
        self.conn.commit()

        # Should update 0 rows
        self.cursor.execute("SELECT changes()")
        changes = self.cursor.fetchone()[0]

        self.assertEqual(changes, 0, "Updating a non-existent student should not modify any row")

    def test_update_missing_required_field_fails(self):
        # Insert valid student
        self.cursor.execute("""
            INSERT INTO students VALUES
            (1, 'Alice', 'Brown', 'alice@uni.com', 'tutor@uni.com', 'Mom', '07123456789')
        """)
        self.conn.commit()

        # Attempt to set NOT NULL field to NULL
        with self.assertRaises(sqlite3.IntegrityError):
            self.cursor.execute("""
                UPDATE students
                SET first_name = NULL
                WHERE student_id = 1
            """)

    def test_update_student_id_not_allowed(self):
        # Insert test student
        self.cursor.execute("""
            INSERT INTO students VALUES
            (1, 'Alice', 'Brown', 'alice@uni.com', 'tutor@uni.com', 'Mom', '07123456789')
        """)
        self.conn.commit()

        # Attempt to change primary key to one that already exists
        self.cursor.execute("""
            INSERT INTO students VALUES
            (2, 'Bob', 'Smith', 'bob@uni.com', 'tutor@uni.com', 'Dad', '07999999999')
        """)
        self.conn.commit()

        with self.assertRaises(sqlite3.IntegrityError):
            self.cursor.execute("""
                UPDATE students
                SET student_id = 2
                WHERE student_id = 1
            """)

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
    
    def test_delete_nonexistent_student_no_error(self):
        # Test that deleting a student who does NOT exist does not raise an error.
        try:
            self.cursor.execute("DELETE FROM students WHERE student_id = 999")
            self.conn.commit()
        except Exception:
            self.fail("Deleting a non-existing student should NOT raise an exception.")

        # Verify that 0 rows were affected
        self.cursor.execute("SELECT changes()")
        rows_affected = self.cursor.fetchone()[0]

        self.assertEqual(rows_affected, 0, "Deleting a nonexistent student should affect 0 rows")



if __name__ == '__main__':
    unittest.main()
