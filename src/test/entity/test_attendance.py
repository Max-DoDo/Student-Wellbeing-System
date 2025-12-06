import unittest
from base.entity.attendance import Attendance # Use the real Attendance entity

class TestAttendanceEntity(unittest.TestCase):

    def test_initialization_values(self):
        a = Attendance(
            attendance_id=10,
            student_id=20,
            week_number=3,
            is_present=True,
            is_late=False
        )
        self.assertEqual(a.attendance_id, 10)
        self.assertEqual(a.student_id, 20)
        self.assertEqual(a.week_number, 3)
        self.assertTrue(a.is_present)
        self.assertFalse(a.is_late)

    def test_none_fields(self):
        a = Attendance(
            attendance_id=None,
            student_id=None,
            week_number=None,
            is_present=None,
            is_late=None
        )
        self.assertIsNone(a.attendance_id)
        self.assertIsNone(a.student_id)
        self.assertIsNone(a.week_number)
        self.assertIsNone(a.is_present)
        self.assertIsNone(a.is_late)

    def test_equality(self):
        a1 = Attendance(1, 1, 1, True, False)
        a2 = Attendance(1, 1, 1, True, False)
        self.assertEqual(a1, a2)

    def test_string_representation(self):
        a = Attendance(10, 20, 3, True, False)
        self.assertIn("10", str(a))
        self.assertIn("20", str(a))

if __name__ == '__main__':
    unittest.main()
