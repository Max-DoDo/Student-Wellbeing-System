import unittest
from unittest.mock import MagicMock
from base.services.user_service import user_service
from base.entity.wellbeing_survey import Wellbeing_Survey

class TestUserService(unittest.TestCase):

    def setUp(self):
        self.wellbeing_repo = MagicMock()
        self.service = user_service(wellbeing_survey_repo=self.wellbeing_repo)

    def test_addWellbeingSurvey_success(self):
        survey = Wellbeing_Survey(
            survey_id=-1,
            student_id=1,
            week_number=5,
            stress_level=3,
            hours_slept=7.5,
            survey_date="2024-01-15"
        )
        self.wellbeing_repo.addWellbeingSurvey.return_value = 100

        result = self.service.addWellbeingSurvey(survey)

        self.assertEqual(result, 100)
        self.wellbeing_repo.addWellbeingSurvey.assert_called_once_with(survey)

    def test_addWellbeingSurvey_with_all_fields(self):
        survey = Wellbeing_Survey(
            survey_id=50,
            student_id=2,
            week_number=10,
            stress_level=5,
            hours_slept=4.0,
            survey_date="2024-02-20"
        )
        self.wellbeing_repo.addWellbeingSurvey.return_value = 50

        result = self.service.addWellbeingSurvey(survey)

        self.assertEqual(result, 50)
        self.wellbeing_repo.addWellbeingSurvey.assert_called_once_with(survey)

    def test_addWellbeingSurvey_low_stress(self):
        survey = Wellbeing_Survey(
            survey_id=-1,
            student_id=3,
            week_number=1,
            stress_level=1,
            hours_slept=9.0,
            survey_date="2024-03-01"
        )
        self.wellbeing_repo.addWellbeingSurvey.return_value = 101

        result = self.service.addWellbeingSurvey(survey)

        self.assertEqual(result, 101)
        self.wellbeing_repo.addWellbeingSurvey.assert_called_once_with(survey)

    def test_addWellbeingSurvey_high_stress(self):
        survey = Wellbeing_Survey(
            survey_id=-1,
            student_id=4,
            week_number=8,
            stress_level=5,
            hours_slept=3.5,
            survey_date="2024-03-15"
        )
        self.wellbeing_repo.addWellbeingSurvey.return_value = 102

        result = self.service.addWellbeingSurvey(survey)

        self.assertEqual(result, 102)
        self.wellbeing_repo.addWellbeingSurvey.assert_called_once_with(survey)


if __name__ == "__main__":
    unittest.main()
