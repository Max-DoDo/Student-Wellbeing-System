import unittest
from base.repository.attendance_repo import Attendance_Repo
from base.entity.attendance import Attendance
from test_refactored.base_repository_test import BaseRepositoryTest

class TestAttendanceRepo(BaseRepositoryTest):

    def setUp(self):
        self.repo = Attendance_Repo()

    def test_getAttendance(self):
        """Test getting a single attendance record by ID."""
        a = self.repo.getAttendance(1)
        self.assertIsNotNone(a)
        # self.assertEqual(a.attendance_id, 1)

    def test_getAttendance_not_found(self):
        """Test retrieving a non-existing attendance ID returns None."""
        a = self.repo.getAttendance(9999)
        self.assertIsNone(a)

    def test_getAllAttendance(self):
        """Test retrieving all attendance records."""
        rows = self.repo.getAllAttendance()
        self.assertIsInstance(rows, list)
        self.assertGreater(len(rows), 0)

if __name__ == "__main__":
    unittest.main()
