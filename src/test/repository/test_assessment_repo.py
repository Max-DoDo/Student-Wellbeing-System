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

if __name__ == "__main__":
    unittest.main()
