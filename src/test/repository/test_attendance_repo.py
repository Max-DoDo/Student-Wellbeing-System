import unittest
from base.repository.attendance_repo import Attendance_Repo
from base.entity.attendance import Attendance
from test.base_repository_test import BaseRepositoryTest

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

    def test_addAttendance_auto_id(self):
        attendance = Attendance(
            attendance_id=None,
            student_id=1,
            week_number=20,
            is_present=True,
            is_late=False
        )
        attendance_id = self.repo.addAttendance(attendance)
        self.assertIsNotNone(attendance_id)
        self.assertGreater(attendance_id, 0)

        # Verify the attendance was added
        added_attendance = self.repo.getAttendance(attendance_id)
        self.assertIsNotNone(added_attendance)
        self.assertEqual(added_attendance.student_id, 1)
        self.assertEqual(added_attendance.week_number, 20)
        self.assertEqual(added_attendance.is_present, True)
        self.assertEqual(added_attendance.is_late, False)

    def test_addAttendance_present_and_late(self):
        attendance = Attendance(
            attendance_id=None,
            student_id=2,
            week_number=15,
            is_present=True,
            is_late=True
        )
        attendance_id = self.repo.addAttendance(attendance)
        self.assertIsNotNone(attendance_id)

        added_attendance = self.repo.getAttendance(attendance_id)
        self.assertEqual(added_attendance.is_present, True)
        self.assertEqual(added_attendance.is_late, True)

    def test_addAttendance_absent(self):
        attendance = Attendance(
            attendance_id=None,
            student_id=3,
            week_number=10,
            is_present=False,
            is_late=False
        )
        attendance_id = self.repo.addAttendance(attendance)
        self.assertIsNotNone(attendance_id)

        added_attendance = self.repo.getAttendance(attendance_id)
        self.assertEqual(added_attendance.is_present, False)
        self.assertEqual(added_attendance.is_late, False)

    def test_addAttendance_missing_student_id(self):
        attendance = Attendance(
            attendance_id=None,
            student_id=None,
            week_number=5,
            is_present=True,
            is_late=False
        )
        with self.assertRaises(ValueError) as context:
            self.repo.addAttendance(attendance)
        self.assertIn("Missing required attendance fields", str(context.exception))

    def test_addAttendance_missing_week_number(self):
        attendance = Attendance(
            attendance_id=None,
            student_id=1,
            week_number=None,
            is_present=True,
            is_late=False
        )
        with self.assertRaises(ValueError) as context:
            self.repo.addAttendance(attendance)
        self.assertIn("Missing required attendance fields", str(context.exception))

    def test_addAttendance_missing_is_present(self):
        attendance = Attendance(
            attendance_id=None,
            student_id=1,
            week_number=5,
            is_present=None,
            is_late=False
        )
        with self.assertRaises(ValueError) as context:
            self.repo.addAttendance(attendance)
        self.assertIn("Missing required attendance fields", str(context.exception))

    def test_addAttendance_missing_is_late(self):
        attendance = Attendance(
            attendance_id=None,
            student_id=1,
            week_number=5,
            is_present=True,
            is_late=None
        )
        with self.assertRaises(ValueError) as context:
            self.repo.addAttendance(attendance)
        self.assertIn("Missing required attendance fields", str(context.exception))

    def test_addAttendance_boundary_week_min(self):
        attendance = Attendance(
            attendance_id=None,
            student_id=1,
            week_number=1,
            is_present=True,
            is_late=False
        )
        attendance_id = self.repo.addAttendance(attendance)
        self.assertIsNotNone(attendance_id)

        added_attendance = self.repo.getAttendance(attendance_id)
        self.assertEqual(added_attendance.week_number, 1)

    def test_addAttendance_boundary_week_max(self):
        attendance = Attendance(
            attendance_id=None,
            student_id=1,
            week_number=52,
            is_present=True,
            is_late=False
        )
        attendance_id = self.repo.addAttendance(attendance)
        self.assertIsNotNone(attendance_id)

        added_attendance = self.repo.getAttendance(attendance_id)
        self.assertEqual(added_attendance.week_number, 52)

if __name__ == "__main__":
    unittest.main()
