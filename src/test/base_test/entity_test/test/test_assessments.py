import unittest
import os

# ===========================================================================
# PLACEHOLDERS (STUBS)
# ===========================================================================

from base_test.entity_test.assessments_test import Assessment_test

def create_assessment_test(aid, sid, name, grade, date):
    return Assessment_test(
        assessment_id_test=aid,
        student_id_test=sid,
        assignment_name_test=name,
        grade_test=grade,
        submitted_on_time_test=date
    )

def create_assessment_none_date():
    return Assessment_test(
        assessment_id_test=1,
        student_id_test=1,
        assignment_name_test="Test",
        grade_test=80,
        submitted_on_time_test=None
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

        self.assertEqual(a.assessment_id_test, 10)
        self.assertEqual(a.student_id_test, 20)
        self.assertEqual(a.assignment_name_test, "Homework")
        self.assertEqual(a.grade_test, 90)
        self.assertEqual(a.submitted_on_time_test, "2025-01-01")

    def test_none_date(self):
        """Test that submitted_on_time_test is set when None is provided."""
        a = create_assessment_none_date()
        self.assertIsNotNone(a.submitted_on_time_test)

    def test_instance_type(self):
        """Test that the object is an instance of the expected class."""
        a = create_assessment_test(1, 2, "A", 88, "2024-01-01")
        self.assertIsInstance(a, Assessment_test)


if __name__ == '__main__':
    unittest.main()
