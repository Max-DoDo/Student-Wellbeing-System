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

    def test_addWellbeingSurvey_auto_id(self):
        survey = Wellbeing_Survey(
            survey_id=-1,
            student_id=1,
            week_number=15,
            stress_level=3,
            hours_slept=7.5,
            survey_date="2024-04-01"
        )
        survey_id = self.repo.addWellbeingSurvey(survey)
        self.assertIsNotNone(survey_id)
        self.assertGreater(survey_id, 0)

        # Verify the survey was added
        added_survey = self.repo.getWellBeingSurvey(survey_id)
        self.assertIsNotNone(added_survey)
        self.assertEqual(added_survey.student_id, 1)
        self.assertEqual(added_survey.week_number, 15)
        self.assertEqual(added_survey.stress_level, 3)
        self.assertEqual(added_survey.hours_slept, 7.5)

    def test_addWellbeingSurvey_missing_student_id(self):
        survey = Wellbeing_Survey(
            survey_id=-1,
            student_id=-1,
            week_number=5,
            stress_level=3,
            hours_slept=7.0
        )
        with self.assertRaises(ValueError) as context:
            self.repo.addWellbeingSurvey(survey)
        self.assertIn("Missing required wellbeing survey fields", str(context.exception))

    def test_addWellbeingSurvey_missing_week_number(self):
        survey = Wellbeing_Survey(
            survey_id=-1,
            student_id=1,
            week_number=-1,
            stress_level=3,
            hours_slept=7.0
        )
        with self.assertRaises(ValueError) as context:
            self.repo.addWellbeingSurvey(survey)
        self.assertIn("Missing required wellbeing survey fields", str(context.exception))

    def test_addWellbeingSurvey_missing_stress_level(self):
        survey = Wellbeing_Survey(
            survey_id=-1,
            student_id=1,
            week_number=5,
            stress_level=-1,
            hours_slept=7.0
        )
        with self.assertRaises(ValueError) as context:
            self.repo.addWellbeingSurvey(survey)
        self.assertIn("Missing required wellbeing survey fields", str(context.exception))

    def test_addWellbeingSurvey_missing_hours_slept(self):
        survey = Wellbeing_Survey(
            survey_id=-1,
            student_id=1,
            week_number=5,
            stress_level=3,
            hours_slept=-1
        )
        with self.assertRaises(ValueError) as context:
            self.repo.addWellbeingSurvey(survey)
        self.assertIn("Missing required wellbeing survey fields", str(context.exception))

    def test_addWellbeingSurvey_boundary_stress_min(self):
        survey = Wellbeing_Survey(
            survey_id=-1,
            student_id=1,
            week_number=5,
            stress_level=1,
            hours_slept=8.0,
            survey_date="2024-04-02"
        )
        survey_id = self.repo.addWellbeingSurvey(survey)
        self.assertIsNotNone(survey_id)

        added_survey = self.repo.getWellBeingSurvey(survey_id)
        self.assertEqual(added_survey.stress_level, 1)

    def test_addWellbeingSurvey_boundary_stress_max(self):
        survey = Wellbeing_Survey(
            survey_id=-1,
            student_id=1,
            week_number=5,
            stress_level=5,
            hours_slept=4.0,
            survey_date="2024-04-03"
        )
        survey_id = self.repo.addWellbeingSurvey(survey)
        self.assertIsNotNone(survey_id)

        added_survey = self.repo.getWellBeingSurvey(survey_id)
        self.assertEqual(added_survey.stress_level, 5)

    def test_addWellbeingSurvey_boundary_hours_min(self):
        survey = Wellbeing_Survey(
            survey_id=-1,
            student_id=1,
            week_number=5,
            stress_level=3,
            hours_slept=0.0,
            survey_date="2024-04-04"
        )
        survey_id = self.repo.addWellbeingSurvey(survey)
        self.assertIsNotNone(survey_id)

        added_survey = self.repo.getWellBeingSurvey(survey_id)
        self.assertEqual(added_survey.hours_slept, 0.0)

    def test_addWellbeingSurvey_boundary_hours_max(self):
        survey = Wellbeing_Survey(
            survey_id=-1,
            student_id=1,
            week_number=5,
            stress_level=3,
            hours_slept=24.0,
            survey_date="2024-04-05"
        )
        survey_id = self.repo.addWellbeingSurvey(survey)
        self.assertIsNotNone(survey_id)

        added_survey = self.repo.getWellBeingSurvey(survey_id)
        self.assertEqual(added_survey.hours_slept, 24.0)

if __name__ == "__main__":
    unittest.main()
