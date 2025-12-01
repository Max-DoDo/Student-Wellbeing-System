import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ===========================================================================
# PLACEHOLDERS (STUBS)
# ===========================================================================

from attendance_test import Attendance_test

def create_attendance_test(aid, sid, week, present, late):
    return Attendance_test(
        attendance_id_test=aid,
        student_id_test=sid,
        week_number_test=week,
        is_present_test=present,
        is_late_test=late
    )

def create_attendance_none_values():
    return Attendance_test(
        attendance_id_test=None,
        student_id_test=None,
        week_number_test=None,
        is_present_test=None,
        is_late_test=None
    )

# ===========================================================================
# END PLACEHOLDERS
# ===========================================================================


class TestAttendanceEntity(unittest.TestCase):

    def setUp(self):
        self.tmp = "temp_file.tmp"
        with open(self.tmp, "w") as f:
            f.write("x")

    def tearDown(self):
        if os.path.exists(self.tmp):
            os.remove(self.tmp)

    def test_initialization_values(self):
        """Test that provided values are assigned correctly."""
        a = create_attendance_test(
            aid=10,
            sid=20,
            week=3,
            present=True,
            late=False
        )

        self.assertEqual(a.attendance_id_test, 10)
        self.assertEqual(a.student_id_test, 20)
        self.assertEqual(a.week_number_test, 3)
        self.assertTrue(a.is_present_test)
        self.assertFalse(a.is_late_test)

    def test_none_fields(self):
        """Test creating an object with None fields."""
        a = create_attendance_none_values()

        self.assertIsNone(a.attendance_id_test)
        self.assertIsNone(a.student_id_test)
        self.assertIsNone(a.week_number_test)
        self.assertIsNone(a.is_present_test)
        self.assertIsNone(a.is_late_test)

    def test_instance_type(self):
        """Test that the object is an instance of the expected class."""
        a = create_attendance_test(1, 2, 1, True, False)
        self.assertIsInstance(a, Attendance_test)


if __name__ == '__main__':
    unittest.main()
