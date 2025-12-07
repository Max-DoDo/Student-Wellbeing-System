import unittest
from base.repository.assessment_repo import Assessment_Repo
from base.entity.assessments import Assessment
from test.base_repository_test import BaseRepositoryTest

class TestAssessmentRepo(BaseRepositoryTest):

    def setUp(self):
        self.repo = Assessment_Repo()

    def test_getAssessment(self):
        """Test fetching a single assessment by ID."""
        a = self.repo.getAssessment(1)
        self.assertIsNotNone(a)
        # Assuming some data exists in the db, we can make assertions
        # self.assertEqual(a.assessment_id, 1)

    def test_getAssessment_not_found(self):
        """Test fetching an ID that does not exist returns None."""
        a = self.repo.getAssessment(9999) # Use a high number to ensure not found
        self.assertIsNone(a)

    def test_getAssessments(self):
        """Test fetching all assessments returns list with correct items."""
        items = self.repo.getAssessments()
        self.assertIsInstance(items, list)
        self.assertGreater(len(items), 0) # Assuming there's at least one assessment

    def test_addAssessment_auto_id(self):
        assessment = Assessment(
            assessment_id=None,
            student_id=1,
            assignment_name="Final Exam",
            grade=92,
            submitted_on_time=1
        )
        assessment_id = self.repo.addAssessment(assessment)
        self.assertIsNotNone(assessment_id)
        self.assertGreater(assessment_id, 0)

        # Verify the assessment was added
        added_assessment = self.repo.getAssessment(assessment_id)
        self.assertIsNotNone(added_assessment)
        self.assertEqual(added_assessment.student_id, 1)
        self.assertEqual(added_assessment.assignment_name, "Final Exam")
        self.assertEqual(added_assessment.grade, 92)
        self.assertEqual(added_assessment.submitted_on_time, 1)

    def test_addAssessment_submitted_late(self):
        assessment = Assessment(
            assessment_id=None,
            student_id=2,
            assignment_name="Late Assignment",
            grade=75,
            submitted_on_time=0
        )
        assessment_id = self.repo.addAssessment(assessment)
        self.assertIsNotNone(assessment_id)

        added_assessment = self.repo.getAssessment(assessment_id)
        self.assertEqual(added_assessment.submitted_on_time, 0)
        self.assertEqual(added_assessment.grade, 75)

    def test_addAssessment_missing_student_id(self):
        assessment = Assessment(
            assessment_id=None,
            student_id=None,
            assignment_name="Test",
            grade=80,
            submitted_on_time=1
        )
        with self.assertRaises(ValueError) as context:
            self.repo.addAssessment(assessment)
        self.assertIn("Missing required assessment fields", str(context.exception))

    def test_addAssessment_missing_assignment_name(self):
        assessment = Assessment(
            assessment_id=None,
            student_id=1,
            assignment_name=None,
            grade=80,
            submitted_on_time=1
        )
        with self.assertRaises(ValueError) as context:
            self.repo.addAssessment(assessment)
        self.assertIn("Missing required assessment fields", str(context.exception))

    def test_addAssessment_missing_grade(self):
        assessment = Assessment(
            assessment_id=None,
            student_id=1,
            assignment_name="Test",
            grade=None,
            submitted_on_time=1
        )
        with self.assertRaises(ValueError) as context:
            self.repo.addAssessment(assessment)
        self.assertIn("Missing required assessment fields", str(context.exception))

    def test_addAssessment_missing_submitted_on_time(self):
        assessment = Assessment(
            assessment_id=None,
            student_id=1,
            assignment_name="Test",
            grade=80,
            submitted_on_time=""
        )
        with self.assertRaises(ValueError) as context:
            self.repo.addAssessment(assessment)
        self.assertIn("Missing required assessment fields", str(context.exception))

    def test_addAssessment_boundary_grade_min(self):
        assessment = Assessment(
            assessment_id=None,
            student_id=1,
            assignment_name="Poor Assignment",
            grade=0,
            submitted_on_time=1
        )
        assessment_id = self.repo.addAssessment(assessment)
        self.assertIsNotNone(assessment_id)

        added_assessment = self.repo.getAssessment(assessment_id)
        self.assertEqual(added_assessment.grade, 0)

    def test_addAssessment_boundary_grade_max(self):
        assessment = Assessment(
            assessment_id=None,
            student_id=1,
            assignment_name="Perfect Assignment",
            grade=100,
            submitted_on_time=1
        )
        assessment_id = self.repo.addAssessment(assessment)
        self.assertIsNotNone(assessment_id)

        added_assessment = self.repo.getAssessment(assessment_id)
        self.assertEqual(added_assessment.grade, 100)

    def test_addAssessment_various_assignment_names(self):
        assignments = [
            ("Midterm Exam", 85),
            ("Group Project", 90),
            ("Lab Report", 88)
        ]

        for name, grade in assignments:
            assessment = Assessment(
                assessment_id=None,
                student_id=1,
                assignment_name=name,
                grade=grade,
                submitted_on_time=1
            )
            assessment_id = self.repo.addAssessment(assessment)
            self.assertIsNotNone(assessment_id)

            added_assessment = self.repo.getAssessment(assessment_id)
            self.assertEqual(added_assessment.assignment_name, name)
            self.assertEqual(added_assessment.grade, grade)

if __name__ == "__main__":
    unittest.main()
