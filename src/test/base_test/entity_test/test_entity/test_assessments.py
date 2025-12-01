import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ===========================================================================
# PLACEHOLDERS (STUBS)
# ===========================================================================

from assessments_test import Assessment_test

def create_assessment_test(aid, sid, name, grade, date):
    return Assessment_test(
        assessment_id=aid,
        student_id=sid,
        assignment_name=name,
        grade=grade,
        submitted_on_time=date
    )


def create_assessment_none_date():
    return Assessment_test(
        assessment_id=1,
        student_id=1,
        assignment_name="Test",
        grade=80,
        submitted_on_time=None
    )


# ===========================================================================
# END PLACEHOLDERS
# ===========================================================================


class TestAssessmentEntity(unittest.TestCase):

    def setUp(self):
        self.tmp = "temp_file.tmp"
        with open(self.tmp, "w") as f:
            f.write("x")

    def tearDown(self):
        if os.path.exists(self.tmp):
            os.remove(self.tmp)

    def test_initialization(self):
        """Test that all fields are assigned correctly when values are provided."""
        a = create_assessment_test(
            aid=10,
            sid=20,
            name="Homework",
            grade=90,
            date="2025-01-01"
        )

        self.assertEqual(a.assessment_id, 10)
        self.assertEqual(a.student_id, 20)
        self.assertEqual(a.assignment_name, "Homework")
        self.assertEqual(a.grade, 90)
        self.assertEqual(a.submitted_on_time, "2025-01-01")

    def test_none_date(self):
        """Test that submitted_on_time is set when None is provided."""
        a = create_assessment_none_date()
        self.assertIsNotNone(a.submitted_on_time)

    def test_instance_type(self):
        """Test that the object is an instance of the expected class."""
        a = create_assessment_test(1, 2, "A", 88, "2024-01-01")
        self.assertIsInstance(a, Assessment_test)


if __name__ == '__main__':
    unittest.main()