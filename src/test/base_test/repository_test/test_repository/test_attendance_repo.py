import unittest
import sqlite3
import sys
import os

CURRENT_DIR = os.path.dirname(__file__)
SRC_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", ".." ,".."))
sys.path.insert(0, SRC_PATH)

from test.base_test.repository_test.attendance_repo_test import Attendance_Repo_test
from test.base_test.entity_test.attendance_test import Attendance_test
from test.base_test.repository_test.base_repo_test import Base_Repo_test


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


class TestAttendanceRepo(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

        self.conn, self.cursor = setup_test_db()
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

        Base_Repo_test.set_db_path_test(TEST_DB)
        self.repo = Attendance_Repo_test()
        self.repo.conn.row_factory = sqlite3.Row
        self.repo.cursor = self.repo.conn.cursor()

        self.cursor.execute("""
            INSERT INTO attendance
            (attendance_id, student_id, week_number, is_present, is_late)
            VALUES (1, 10, 3, 1, 0)
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

    def test_getAttendance(self):
        """Test getting a single attendance record by ID."""
        a = self.repo.getAttendance(1)

        self.assertIsNotNone(a)
        self.assertEqual(a.attendance_id, 1)
        self.assertEqual(a.student_id, 10)
        self.assertEqual(a.week_number, 3)
        self.assertTrue(a.is_present)
        self.assertFalse(a.is_late)

    def test_getAttendance_not_found(self):
        """Test retrieving a non-existing attendance ID returns None."""
        a = self.repo.getAttendance(999)
        self.assertIsNone(a)

    def test_getAllAttendance(self):
        """Test retrieving all attendance records."""
        rows = self.repo.getAllAttendance()

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].attendance_id, 1)

    def test_getAttendancesByStudentID(self):
        """Test retrieving attendance records by student ID."""
        self.cursor.execute("""
            INSERT INTO attendance
            (attendance_id, student_id, week_number, is_present, is_late)
            VALUES (2, 10, 4, 0, 1)
        """)
        self.conn.commit()

        rows = self.repo.getAttendancesByStudentID(10)

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0].student_id, 10)
        self.assertEqual(rows[1].student_id, 10)

    def test_toAttendance(self):
        """Test converting a DB row into an Attendance_test object."""
        self.cursor.execute("SELECT * FROM attendance WHERE attendance_id = 1")
        row = self.cursor.fetchone()

        obj = self.repo.toAttendance(row)

        self.assertIsInstance(obj, Attendance_test)
        self.assertEqual(obj.attendance_id, 1)

    def test_toAttendances(self):
        """Test converting multiple DB rows."""
        self.cursor.execute("SELECT * FROM attendance")
        rows = self.cursor.fetchall()

        result = self.repo.toAttendances(rows)

        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], Attendance_test)


if __name__ == "__main__":
    unittest.main()
