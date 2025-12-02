import unittest
import sys
import os

CURRENT_DIR = os.path.dirname(__file__)

SRC_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", ".." ,".."))
sys.path.insert(0, SRC_PATH)
from test.base_test.entity_test.attendance_test import Attendance_test


def create_attendance_test(aid, sid, week, present, late):
    return Attendance_test(
        attendance_id=aid,
        student_id=sid,
        week_number=week,
        is_present=present,
        is_late=late
    )


def create_attendance_none_values():
    return Attendance_test(
        attendance_id=None,
        student_id=None,
        week_number=None,
        is_present=None,
        is_late=None
    )


class TestAttendanceEntity(unittest.TestCase):

    def setUp(self):
        self.tmp = "temp_file.tmp"
        with open(self.tmp, "w") as f:
            f.write("x")

    def tearDown(self):
        if os.path.exists(self.tmp):
            os.remove(self.tmp)

    def test_initialization_values(self):
        a = create_attendance_test(10, 20, 3, True, False)

        self.assertEqual(a.attendance_id, 10)
        self.assertEqual(a.student_id, 20)
        self.assertEqual(a.week_number, 3)
        self.assertTrue(a.is_present)
        self.assertFalse(a.is_late)

    def test_none_fields(self):
        a = create_attendance_none_values()

        self.assertIsNone(a.attendance_id)
        self.assertIsNone(a.student_id)
        self.assertIsNone(a.week_number)
        self.assertIsNone(a.is_present)
        self.assertIsNone(a.is_late)

    def test_instance_type(self):
        a = create_attendance_test(1, 2, 1, True, False)
        self.assertIsInstance(a, Attendance_test)


if __name__ == '__main__':
    unittest.main()
