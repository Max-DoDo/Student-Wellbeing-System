import unittest
from base.repository.attendance_repo import Attendance_Repo
from base.entity.attendance import Attendance
from test.base_repository_test import BaseRepositoryTest

class TestAttendanceRepo(BaseRepositoryTest):

    def setUp(self):
        self.repo = Attendance_Repo()

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

    # ========== Invalid Boundary Values Tests ==========

    def test_addAttendance_week_number_zero(self):
        attendance = Attendance(
            attendance_id=None,
            student_id=1,
            week_number=0,
            is_present=True,
            is_late=False
        )
        with self.assertRaises(ValueError):
            self.repo.addAttendance(attendance)

    def test_addAttendance_week_number_negative(self):
        attendance = Attendance(
            attendance_id=None,
            student_id=1,
            week_number=-1,
            is_present=True,
            is_late=False
        )
        with self.assertRaises(ValueError):
            self.repo.addAttendance(attendance)

    def test_addAttendance_week_number_above_max(self):
        attendance = Attendance(
            attendance_id=None,
            student_id=1,
            week_number=53,
            is_present=True,
            is_late=False
        )
        with self.assertRaises(ValueError):
            self.repo.addAttendance(attendance)

    def test_addAttendance_week_number_very_large(self):
        attendance = Attendance(
            attendance_id=None,
            student_id=1,
            week_number=1000000,
            is_present=True,
            is_late=False
        )
        with self.assertRaises(ValueError):
            self.repo.addAttendance(attendance)

    # ========== Boolean Logic Edge Cases Tests ==========

    def test_addAttendance_absent_but_late(self):
        """Test illogical but valid combination: absent but marked late"""
        attendance = Attendance(
            attendance_id=None,
            student_id=1,
            week_number=25,
            is_present=False,
            is_late=True
        )
        attendance_id = self.repo.addAttendance(attendance)
        self.assertIsNotNone(attendance_id)

        added_attendance = self.repo.getAttendance(attendance_id)
        self.assertEqual(added_attendance.is_present, False)
        self.assertEqual(added_attendance.is_late, True)

    # ========== Duplicate and Multiple Records Tests ==========

    def test_addAttendance_duplicate_entry(self):
        """Test adding duplicate attendance for same student/week"""
        # Add first attendance
        attendance1 = Attendance(
            attendance_id=None,
            student_id=1,
            week_number=30,
            is_present=True,
            is_late=False
        )
        attendance_id1 = self.repo.addAttendance(attendance1)

        # Add duplicate (same student, same week) - should succeed
        attendance2 = Attendance(
            attendance_id=None,
            student_id=1,
            week_number=30,
            is_present=False,
            is_late=False
        )
        attendance_id2 = self.repo.addAttendance(attendance2)

        self.assertNotEqual(attendance_id1, attendance_id2)

    def test_addAttendance_multiple_same_student_different_weeks(self):
        """Test adding multiple attendance records for same student"""
        attendance_ids = []
        for week in [31, 32, 33, 34, 35]:
            attendance = Attendance(
                attendance_id=None,
                student_id=2,
                week_number=week,
                is_present=True,
                is_late=False
            )
            attendance_id = self.repo.addAttendance(attendance)
            attendance_ids.append(attendance_id)

        self.assertEqual(len(attendance_ids), 5)
        self.assertEqual(len(set(attendance_ids)), 5)  # All unique IDs

    def test_addAttendance_full_semester(self):
        """Test adding attendance for all 52 weeks"""
        attendance_ids = []
        for week in range(1, 53):
            attendance = Attendance(
                attendance_id=None,
                student_id=3,
                week_number=week,
                is_present=True,
                is_late=False
            )
            attendance_id = self.repo.addAttendance(attendance)
            attendance_ids.append(attendance_id)

        self.assertEqual(len(attendance_ids), 52)
        self.assertEqual(len(set(attendance_ids)), 52)  # All unique IDs

    # ========== Query Tests ==========

    def test_getAttendancesByStudentID_single(self):
        """Test getting attendance for student with one record"""
        attendance = Attendance(
            attendance_id=None,
            student_id=1,
            week_number=40,
            is_present=True,
            is_late=False
        )
        self.repo.addAttendance(attendance)

        attendances = self.repo.getAttendancesByStudentID(1)
        self.assertIsNotNone(attendances)
        self.assertGreater(len(attendances), 0)

    def test_getAttendancesByStudentID_multiple(self):
        """Test getting attendance for student with multiple records"""
        for week in [41, 42, 43]:
            attendance = Attendance(
                attendance_id=None,
                student_id=2,
                week_number=week,
                is_present=True,
                is_late=False
            )
            self.repo.addAttendance(attendance)

        attendances = self.repo.getAttendancesByStudentID(2)
        self.assertIsNotNone(attendances)
        self.assertGreaterEqual(len(attendances), 3)

    def test_getAttendancesByStudentID_nonexistent(self):
        """Test getting attendance for non-existent student"""
        attendances = self.repo.getAttendancesByStudentID(99999)
        self.assertIsNone(attendances)

    def test_getAttendance_negative_id(self):
        """Test getting attendance with negative ID"""
        attendance = self.repo.getAttendance(-1)
        self.assertIsNone(attendance)

    def test_getAllAttendance_verify_count(self):
        """Test that getAllAttendance returns expected number of records"""
        initial_count = len(self.repo.getAllAttendance())

        # Add 3 new attendances
        for week in [44, 45, 46]:
            attendance = Attendance(
                attendance_id=None,
                student_id=1,
                week_number=week,
                is_present=True,
                is_late=False
            )
            self.repo.addAttendance(attendance)

        final_count = len(self.repo.getAllAttendance())
        self.assertEqual(final_count, initial_count + 3)

    # ========== Delete Tests ==========

    def test_deleteAttendanceByStudentID_single(self):
        """Test deleting single attendance record"""
        attendance = Attendance(
            attendance_id=None,
            student_id=1,
            week_number=47,
            is_present=True,
            is_late=False
        )
        attendance_id = self.repo.addAttendance(attendance)

        # Verify it exists
        self.assertIsNotNone(self.repo.getAttendance(attendance_id))

        # Delete
        self.repo.deleteAttendanceByStudentID(1)

    def test_deleteAttendanceByStudentID_multiple(self):
        """Test deleting multiple attendance records"""
        attendance_ids = []
        for week in [48, 49, 50]:
            attendance = Attendance(
                attendance_id=None,
                student_id=3,
                week_number=week,
                is_present=True,
                is_late=False
            )
            attendance_id = self.repo.addAttendance(attendance)
            attendance_ids.append(attendance_id)

        # Delete all attendances for student 3
        self.repo.deleteAttendanceByStudentID(3)

        # Verify all are deleted
        for attendance_id in attendance_ids:
            self.assertIsNone(self.repo.getAttendance(attendance_id))

    def test_deleteAttendanceByStudentID_nonexistent(self):
        """Test deleting attendance for non-existent student doesn't crash"""
        try:
            self.repo.deleteAttendanceByStudentID(99999)
        except Exception as e:
            self.fail(f"Delete for nonexistent student raised exception: {e}")

    def test_deleteAttendanceByStudentID_verify_cascade(self):
        """Test that delete only affects target student's records"""
        # Add attendance for two different students
        attendance1 = Attendance(
            attendance_id=None,
            student_id=1,
            week_number=51,
            is_present=True,
            is_late=False
        )
        attendance_id1 = self.repo.addAttendance(attendance1)

        attendance2 = Attendance(
            attendance_id=None,
            student_id=2,
            week_number=51,
            is_present=True,
            is_late=False
        )
        attendance_id2 = self.repo.addAttendance(attendance2)

        # Delete attendance for student 1
        self.repo.deleteAttendanceByStudentID(1)

        # Verify student 2's attendance still exists
        remaining_attendance = self.repo.getAttendance(attendance_id2)
        self.assertIsNotNone(remaining_attendance)
        self.assertEqual(remaining_attendance.student_id, 2)

    # ========== Edge Cases Tests ==========

    def test_addAttendance_specified_id(self):
        """Test manually specifying attendance_id"""
        attendance = Attendance(
            attendance_id=50000,
            student_id=1,
            week_number=26,
            is_present=True,
            is_late=False
        )
        attendance_id = self.repo.addAttendance(attendance)
        self.assertEqual(attendance_id, 50000)

        # Verify it was added with that ID
        added_attendance = self.repo.getAttendance(50000)
        self.assertIsNotNone(added_attendance)
        self.assertEqual(added_attendance.attendance_id, 50000)

    def test_addAttendance_all_combinations(self):
        """Test all 4 combinations of is_present/is_late"""
        combinations = [
            (True, True),   # present and late
            (True, False),  # present and on time
            (False, True),  # absent but late (illogical)
            (False, False)  # absent and not late
        ]

        for i, (is_present, is_late) in enumerate(combinations):
            attendance = Attendance(
                attendance_id=None,
                student_id=1,
                week_number=i + 1,
                is_present=is_present,
                is_late=is_late
            )
            attendance_id = self.repo.addAttendance(attendance)
            self.assertIsNotNone(attendance_id)

            added_attendance = self.repo.getAttendance(attendance_id)
            self.assertEqual(added_attendance.is_present, is_present)
            self.assertEqual(added_attendance.is_late, is_late)

if __name__ == "__main__":
    unittest.main()
