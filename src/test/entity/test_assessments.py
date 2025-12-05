import unittest
from base.entity.assessments import Assessment

class TestAssessmentEntity(unittest.TestCase):

    def test_initialization(self):
        """Test that all fields are assigned correctly when values are provided."""
        a = Assessment(
            assessment_id=10,
            student_id=20,
            assignment_name="Homework",
            grade=90,
            submitted_on_time="2025-01-01"
        )
        self.assertEqual(a.assessment_id, 10)
        self.assertEqual(a.student_id, 20)
        self.assertEqual(a.assignment_name, "Homework")
        self.assertEqual(a.grade, 90)
        self.assertEqual(a.submitted_on_time, "2025-01-01")

if __name__ == '__main__':
    unittest.main()
