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
    
    def test_initialization_with_none(self):
        """Test that all fields are assigned correctly when values are None."""
        a = Assessment(
            assessment_id=None,
            student_id=None,
            assignment_name=None,
            grade=None,
            submitted_on_time=None
        )
        self.assertIsNone(a.assessment_id)
        self.assertIsNone(a.student_id)
        self.assertIsNone(a.assignment_name)
        self.assertIsNone(a.grade)
        self.assertIsNotNone(a.submitted_on_time) # default value check

    def test_grade_boundaries(self):
        a_min = Assessment(1, 1, "Min", grade=0, submitted_on_time="2025-01-01")
        a_max = Assessment(1, 1, "Max", grade=100, submitted_on_time="2025-01-01")
        
        self.assertEqual(a_min.grade, 0)
        self.assertEqual(a_max.grade, 100)

if __name__ == '__main__':
    unittest.main()
