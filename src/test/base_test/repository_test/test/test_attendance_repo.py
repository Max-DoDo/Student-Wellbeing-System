import unittest
import os
import sqlite3

# ===========================================================================
# PLACEHOLDERS (STUBS)
# ===========================================================================

from repository_test.attendance_repo_test import Attendance_Repo_test
from entity_test.attendance_test import Attendance_test
from repository_test.base_repo_test import Base_Repo_test

TEST_DB = "test_attendance_repo.db"

def setup_test_db():
    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE attendance (
            attendance_id INTEGER PRIMARY KEY,
            student_id INTEGER,
            week_number INTEGER,
            is_present INTEGER,
            is_late INTEGER
        );
    """)
    conn.commit()
    return conn, cursor

# ===========================================================================
# END PLACEHOLDERS
# ===========================================================================


class TestAttendanceRepo(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

        self.conn, self.cursor = setup_test_db()
        Base_Repo_test.DB_PATH = TEST_DB
        self.repo = Attendance_Repo_test()

        # Insert initial test row
        self.cursor.execute("""
            INSERT INTO attendance
            (attendance_id, student_id, week_number, is_present, is_late)
            VALUES (1, 10, 3, 1, 0)
        """)
        self.conn.commit()

    def tearDown(self):
        self.conn.close()
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_getAttendance_test(self):
        """Test getting a single attendance record by ID."""
        a = self.repo.getAttendance_test(1)

        self.assertIsNotNone(a)
        self.assertEqual(a.attendance_id_test, 1)
        self.assertEqual(a.student_id_test, 10)
        self.assertEqual(a.week_number_test, 3)
        self.assertTrue(a.is_present_test)
        self.assertFalse(a.is_late_test)

    def test_getAttendance_test_not_found(self):
        """Test retrieving a non-existing attendance ID returns None."""
        a = self.repo.getAttendance_test(999)
        self.assertIsNone(a)

    def test_getAllAttendance_test(self):
        """Test retrieving all attendance records."""
        rows = self.repo.getAllAttendance_test()

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].attendance_id_test, 1)

    def test_getAttendancesByStudentID_test(self):
        """Test retrieving attendance records by student ID."""
        # Insert another row
        self.cursor.execute("""
            INSERT INTO attendance
            (attendance_id, student_id, week_number, is_present, is_late)
            VALUES (2, 10, 4, 0, 1)
        """)
        self.conn.commit()

        rows = self.repo.getAttendancesByStudentID_test(10)

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0].student_id_test, 10)
        self.assertEqual(rows[1].student_id_test, 10)

    def test_toAttendance_test(self):
        """Test converting a DB row into an Attendance_test object."""
        self.cursor.execute("SELECT * FROM attendance WHERE attendance_id = 1")
        row = self.cursor.fetchone()

        obj = self.repo.toAttendance_test(row)

        self.assertIsInstance(obj, Attendance_test)
        self.assertEqual(obj.attendance_id_test, 1)

    def test_toAttendances_test(self):
        """Test converting multiple DB rows into Attendance_test objects."""
        self.cursor.execute("SELECT * FROM attendance")
        rows = self.cursor.fetchall()

        result = self.repo.toAttendances_test(rows)

        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], Attendance_test)


if __name__ == '__main__':
    unittest.main()
