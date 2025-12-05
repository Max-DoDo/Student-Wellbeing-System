import unittest
from test_refactored.base_repository_test import BaseRepositoryTest
from base.repository.wellbeing_surveys_repo import Wellbeing_Survey_Repo

class TestWellbeingFeatures(BaseRepositoryTest):

    def setUp(self):
        super().setUp()
        self.repo = Wellbeing_Survey_Repo()

    def test_retrieve_student_history_trends(self):
        """Test retrieving wellbeing survey history for an existing student."""
        # Assuming student_id 1 exists in university_wellbeing.db and has surveys
        student_id = 1
        history = self.repo.getWellBeingSurveysByStudentID(student_id)
        
        self.assertIsInstance(history, list)
        self.assertGreater(len(history), 0) # Assuming student 1 has some history

    def test_aggregated_wellbeing_metrics(self):
        """Test calculating average stress for a specific week for existing data."""
        # Assuming week 1 has some data for stress levels
        week = 1
        surveys_for_week = [s.stress_level for s in self.repo.getWellBeingSurveys() if s.week_number == week]

        if not surveys_for_week:
            self.skipTest(f"No wellbeing survey data for week {week} in the database.")
            return

        avg_stress = sum(surveys_for_week) / len(surveys_for_week)
        self.assertIsInstance(avg_stress, float)
        self.assertGreater(avg_stress, 0)


if __name__ == '__main__':
    unittest.main()
