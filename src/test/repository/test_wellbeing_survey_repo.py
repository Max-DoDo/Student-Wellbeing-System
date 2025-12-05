import unittest
from base.repository.wellbeing_surveys_repo import Wellbeing_Survey_Repo
from base.entity.wellbeing_survey import Wellbeing_Survey
from test.base_repository_test import BaseRepositoryTest

class TestWellbeingSurveyRepo(BaseRepositoryTest):

    def setUp(self):
        self.repo = Wellbeing_Survey_Repo()

    def test_getWellBeingSurvey(self):
        s = self.repo.getWellBeingSurvey(1)
        self.assertIsNotNone(s)
        # self.assertEqual(s.survey_id, 1)

    def test_getWellBeingSurvey_not_found(self):
        s = self.repo.getWellBeingSurvey(9999)
        self.assertIsNone(s)

    def test_getWellBeingSurveys(self):
        surveys = self.repo.getWellBeingSurveys()
        self.assertIsInstance(surveys, list)
        self.assertGreater(len(surveys), 0)

if __name__ == "__main__":
    unittest.main()
