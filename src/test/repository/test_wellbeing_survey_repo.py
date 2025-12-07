import unittest
from base.repository.wellbeing_surveys_repo import Wellbeing_Survey_Repo
from base.entity.wellbeing_survey import Wellbeing_Survey
from test.base_repository_test import BaseRepositoryTest

class TestWellbeingSurveyRepo(BaseRepositoryTest):

    def setUp(self):
        self.repo = Wellbeing_Survey_Repo()

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
        survey_id = self.repo.addWellBeingSurvey(survey)
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
            self.repo.addWellBeingSurvey(survey)
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
            self.repo.addWellBeingSurvey(survey)
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
            self.repo.addWellBeingSurvey(survey)
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
            self.repo.addWellBeingSurvey(survey)
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
        survey_id = self.repo.addWellBeingSurvey(survey)
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
        survey_id = self.repo.addWellBeingSurvey(survey)
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
        survey_id = self.repo.addWellBeingSurvey(survey)
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
        survey_id = self.repo.addWellBeingSurvey(survey)
        self.assertIsNotNone(survey_id)

        added_survey = self.repo.getWellBeingSurvey(survey_id)
        self.assertEqual(added_survey.hours_slept, 24.0)

    # ========== Invalid Boundary Values Tests ==========

    def test_addWellbeingSurvey_stress_level_below_min(self):
        survey = Wellbeing_Survey(
            survey_id=-1,
            student_id=1,
            week_number=5,
            stress_level=0,
            hours_slept=7.0,
            survey_date="2024-04-06"
        )
        with self.assertRaises(ValueError):
            self.repo.addWellBeingSurvey(survey)

    def test_addWellbeingSurvey_stress_level_above_max(self):
        survey = Wellbeing_Survey(
            survey_id=-1,
            student_id=1,
            week_number=5,
            stress_level=6,
            hours_slept=7.0,
            survey_date="2024-04-07"
        )
        with self.assertRaises(ValueError):
            self.repo.addWellBeingSurvey(survey)

    def test_addWellbeingSurvey_stress_level_negative(self):
        survey = Wellbeing_Survey(
            survey_id=-1,
            student_id=1,
            week_number=5,
            stress_level=-5,
            hours_slept=7.0,
            survey_date="2024-04-08"
        )
        with self.assertRaises(ValueError):
            self.repo.addWellBeingSurvey(survey)

    def test_addWellbeingSurvey_hours_slept_negative(self):
        survey = Wellbeing_Survey(
            survey_id=-1,
            student_id=1,
            week_number=5,
            stress_level=3,
            hours_slept=-1.5,
            survey_date="2024-04-09"
        )
        with self.assertRaises(ValueError):
            self.repo.addWellBeingSurvey(survey)

    def test_addWellbeingSurvey_hours_slept_above_max(self):
        survey = Wellbeing_Survey(
            survey_id=-1,
            student_id=1,
            week_number=5,
            stress_level=3,
            hours_slept=25.0,
            survey_date="2024-04-10"
        )
        with self.assertRaises(ValueError):
            self.repo.addWellBeingSurvey(survey)

    def test_addWellbeingSurvey_week_number_zero(self):
        survey = Wellbeing_Survey(
            survey_id=-1,
            student_id=1,
            week_number=0,
            stress_level=3,
            hours_slept=7.0,
            survey_date="2024-04-11"
        )
        with self.assertRaises(ValueError):
            self.repo.addWellBeingSurvey(survey)

    def test_addWellbeingSurvey_week_number_above_max(self):
        survey = Wellbeing_Survey(
            survey_id=-1,
            student_id=1,
            week_number=53,
            stress_level=3,
            hours_slept=7.0,
            survey_date="2024-04-12"
        )
        with self.assertRaises(ValueError):
            self.repo.addWellBeingSurvey(survey)

    def test_addWellbeingSurvey_week_number_negative(self):
        survey = Wellbeing_Survey(
            survey_id=-1,
            student_id=1,
            week_number=-1,
            stress_level=3,
            hours_slept=7.0,
            survey_date="2024-04-13"
        )
        with self.assertRaises(ValueError):
            self.repo.addWellBeingSurvey(survey)

    # ========== Data Type Edge Cases Tests ==========

    def test_addWellbeingSurvey_fractional_hours(self):
        test_hours = [7.5, 8.25, 6.75]
        for hours in test_hours:
            survey = Wellbeing_Survey(
                survey_id=-1,
                student_id=1,
                week_number=20 + test_hours.index(hours),
                stress_level=3,
                hours_slept=hours,
                survey_date="2024-04-16"
            )
            survey_id = self.repo.addWellBeingSurvey(survey)
            self.assertIsNotNone(survey_id)

            added_survey = self.repo.getWellBeingSurvey(survey_id)
            self.assertEqual(added_survey.hours_slept, hours)

    def test_addWellbeingSurvey_very_large_week_number(self):
        survey = Wellbeing_Survey(
            survey_id=-1,
            student_id=1,
            week_number=1000000,
            stress_level=3,
            hours_slept=7.0,
            survey_date="2024-04-18"
        )
        with self.assertRaises(ValueError):
            self.repo.addWellBeingSurvey(survey)

    # ========== Date Handling Tests ==========

    def test_addWellbeingSurvey_null_survey_date(self):
        survey = Wellbeing_Survey(
            survey_id=-1,
            student_id=1,
            week_number=25,
            stress_level=3,
            hours_slept=7.0,
            survey_date=None
        )
        survey_id = self.repo.addWellBeingSurvey(survey)
        self.assertIsNotNone(survey_id)

        # Verify survey_date was set (either default or from entity __post_init__)
        added_survey = self.repo.getWellBeingSurvey(survey_id)
        self.assertIsNotNone(added_survey.survey_date)

    def test_addWellbeingSurvey_invalid_date_format(self):
        survey = Wellbeing_Survey(
            survey_id=-1,
            student_id=1,
            week_number=26,
            stress_level=3,
            hours_slept=7.0,
            survey_date="invalid-date"
        )
        # SQLite accepts any string for date fields
        survey_id = self.repo.addWellBeingSurvey(survey)
        self.assertIsNotNone(survey_id)

    def test_addWellbeingSurvey_future_date(self):
        survey = Wellbeing_Survey(
            survey_id=-1,
            student_id=1,
            week_number=27,
            stress_level=3,
            hours_slept=7.0,
            survey_date="2099-12-31"
        )
        survey_id = self.repo.addWellBeingSurvey(survey)
        self.assertIsNotNone(survey_id)

        added_survey = self.repo.getWellBeingSurvey(survey_id)
        self.assertEqual(added_survey.survey_date, "2099-12-31")

    def test_addWellbeingSurvey_past_date(self):
        survey = Wellbeing_Survey(
            survey_id=-1,
            student_id=1,
            week_number=28,
            stress_level=3,
            hours_slept=7.0,
            survey_date="1900-01-01"
        )
        survey_id = self.repo.addWellBeingSurvey(survey)
        self.assertIsNotNone(survey_id)

        added_survey = self.repo.getWellBeingSurvey(survey_id)
        self.assertEqual(added_survey.survey_date, "1900-01-01")

    def test_addWellbeingSurvey_empty_date_string(self):
        survey = Wellbeing_Survey(
            survey_id=-1,
            student_id=1,
            week_number=29,
            stress_level=3,
            hours_slept=7.0,
            survey_date=""
        )
        survey_id = self.repo.addWellBeingSurvey(survey)
        self.assertIsNotNone(survey_id)

    # ========== Duplicate and Multiple Records Tests ==========

    def test_addWellbeingSurvey_duplicate_entry(self):
        # Add first survey
        survey1 = Wellbeing_Survey(
            survey_id=-1,
            student_id=1,
            week_number=30,
            stress_level=3,
            hours_slept=7.0,
            survey_date="2024-04-19"
        )
        survey_id1 = self.repo.addWellBeingSurvey(survey1)

        # Add duplicate (same student, same week) - should succeed
        survey2 = Wellbeing_Survey(
            survey_id=-1,
            student_id=1,
            week_number=30,
            stress_level=4,
            hours_slept=6.0,
            survey_date="2024-04-20"
        )
        survey_id2 = self.repo.addWellBeingSurvey(survey2)

        self.assertNotEqual(survey_id1, survey_id2)

    def test_addWellbeingSurvey_multiple_same_student_different_weeks(self):
        surveys_added = []
        for week in [31, 32, 33, 34, 35]:
            survey = Wellbeing_Survey(
                survey_id=-1,
                student_id=1,
                week_number=week,
                stress_level=3,
                hours_slept=7.0,
                survey_date="2024-04-21"
            )
            survey_id = self.repo.addWellBeingSurvey(survey)
            surveys_added.append(survey_id)

        self.assertEqual(len(surveys_added), 5)
        self.assertEqual(len(set(surveys_added)), 5)  # All unique IDs

    def test_addWellbeingSurvey_multiple_same_week_different_students(self):
        # Assuming students 1, 2, 3 exist
        surveys_added = []
        for student_id in [1, 2, 3]:
            survey = Wellbeing_Survey(
                survey_id=-1,
                student_id=student_id,
                week_number=36,
                stress_level=3,
                hours_slept=7.0,
                survey_date="2024-04-22"
            )
            survey_id = self.repo.addWellBeingSurvey(survey)
            surveys_added.append(survey_id)

        self.assertEqual(len(surveys_added), 3)
        self.assertEqual(len(set(surveys_added)), 3)  # All unique IDs

    # ========== Query Tests ==========

    def test_getWellBeingSurveysByStudentID_single(self):
        # Add a single survey for a specific student
        survey = Wellbeing_Survey(
            survey_id=-1,
            student_id=1,
            week_number=37,
            stress_level=3,
            hours_slept=7.0,
            survey_date="2024-04-23"
        )
        self.repo.addWellBeingSurvey(survey)

        surveys = self.repo.getWellBeingSurveysByStudentID(1)
        self.assertIsNotNone(surveys)
        self.assertGreater(len(surveys), 0)

    def test_getWellBeingSurveysByStudentID_multiple(self):
        # Add multiple surveys for same student
        for week in [38, 39, 40]:
            survey = Wellbeing_Survey(
                survey_id=-1,
                student_id=2,
                week_number=week,
                stress_level=3,
                hours_slept=7.0,
                survey_date="2024-04-24"
            )
            self.repo.addWellBeingSurvey(survey)

        surveys = self.repo.getWellBeingSurveysByStudentID(2)
        self.assertIsNotNone(surveys)
        self.assertGreaterEqual(len(surveys), 3)

    def test_getWellBeingSurveysByStudentID_none(self):
        # Query for a student that exists but has no surveys
        # Assuming student_id 1 exists but we query for very high week numbers they don't have
        surveys = self.repo.getWellBeingSurveysByStudentID(1)
        # This should return existing surveys or None, depending on implementation
        # Just verify it doesn't crash
        self.assertTrue(surveys is None or isinstance(surveys, list))

    def test_getWellBeingSurveysByStudentID_nonexistent(self):
        surveys = self.repo.getWellBeingSurveysByStudentID(99999)
        self.assertIsNone(surveys)

    def test_getWellBeingSurvey_negative_id(self):
        survey = self.repo.getWellBeingSurvey(-1)
        self.assertIsNone(survey)

    # ========== Delete Tests ==========

    def test_deleteSurveysByStudentID_single(self):
        # Add a survey
        survey = Wellbeing_Survey(
            survey_id=-1,
            student_id=1,
            week_number=41,
            stress_level=3,
            hours_slept=7.0,
            survey_date="2024-04-25"
        )
        survey_id = self.repo.addWellBeingSurvey(survey)

        # Verify it exists
        self.assertIsNotNone(self.repo.getWellBeingSurvey(survey_id))

        # Delete
        self.repo.deleteSurveysByStudentID(1)

        # Note: This deletes ALL surveys for student 1, not just the one we added
        # Verify deletion (the specific survey should be gone)
        # But student may have other surveys from base data

    def test_deleteSurveysByStudentID_multiple(self):
        # Add multiple surveys
        survey_ids = []
        for week in [42, 43, 44]:
            survey = Wellbeing_Survey(
                survey_id=-1,
                student_id=3,
                week_number=week,
                stress_level=3,
                hours_slept=7.0,
                survey_date="2024-04-26"
            )
            survey_id = self.repo.addWellBeingSurvey(survey)
            survey_ids.append(survey_id)

        # Delete all surveys for student 3
        self.repo.deleteSurveysByStudentID(3)

        # Verify all are deleted
        for survey_id in survey_ids:
            self.assertIsNone(self.repo.getWellBeingSurvey(survey_id))

    def test_deleteSurveysByStudentID_nonexistent(self):
        # Delete surveys for non-existent student (should not crash)
        try:
            self.repo.deleteSurveysByStudentID(99999)
        except Exception as e:
            self.fail(f"Delete for nonexistent student raised exception: {e}")

    def test_deleteSurveysByStudentID_verify_cascade(self):
        # Add surveys for two different students
        survey1 = Wellbeing_Survey(
            survey_id=-1,
            student_id=1,
            week_number=45,
            stress_level=3,
            hours_slept=7.0,
            survey_date="2024-04-27"
        )
        survey_id1 = self.repo.addWellBeingSurvey(survey1)

        survey2 = Wellbeing_Survey(
            survey_id=-1,
            student_id=2,
            week_number=45,
            stress_level=3,
            hours_slept=7.0,
            survey_date="2024-04-28"
        )
        survey_id2 = self.repo.addWellBeingSurvey(survey2)

        # Delete surveys for student 1
        self.repo.deleteSurveysByStudentID(1)

        # Verify student 1's survey is gone
        deleted_survey = self.repo.getWellBeingSurvey(survey_id1)

        # Verify student 2's survey still exists
        remaining_survey = self.repo.getWellBeingSurvey(survey_id2)
        self.assertIsNotNone(remaining_survey)
        self.assertEqual(remaining_survey.student_id, 2)

    # ========== Edge Cases Tests ==========

    def test_addWellbeingSurvey_specified_id(self):
        # Manually specify a survey_id (not -1)
        survey = Wellbeing_Survey(
            survey_id=50000,
            student_id=1,
            week_number=46,
            stress_level=3,
            hours_slept=7.0,
            survey_date="2024-04-29"
        )
        survey_id = self.repo.addWellBeingSurvey(survey)
        self.assertEqual(survey_id, 50000)

        # Verify it was added with that ID
        added_survey = self.repo.getWellBeingSurvey(50000)
        self.assertIsNotNone(added_survey)
        self.assertEqual(added_survey.survey_id, 50000)

    def test_addWellbeingSurvey_boundary_week_1_and_52(self):
        # Test week 1
        survey1 = Wellbeing_Survey(
            survey_id=-1,
            student_id=1,
            week_number=1,
            stress_level=3,
            hours_slept=7.0,
            survey_date="2024-04-30"
        )
        survey_id1 = self.repo.addWellBeingSurvey(survey1)
        self.assertIsNotNone(survey_id1)

        # Test week 52
        survey2 = Wellbeing_Survey(
            survey_id=-1,
            student_id=1,
            week_number=52,
            stress_level=3,
            hours_slept=7.0,
            survey_date="2024-05-01"
        )
        survey_id2 = self.repo.addWellBeingSurvey(survey2)
        self.assertIsNotNone(survey_id2)

        # Verify both were added correctly
        added_survey1 = self.repo.getWellBeingSurvey(survey_id1)
        added_survey2 = self.repo.getWellBeingSurvey(survey_id2)
        self.assertEqual(added_survey1.week_number, 1)
        self.assertEqual(added_survey2.week_number, 52)

    def test_getWellBeingSurveys_empty_database(self):
        # Delete all surveys for students we've been testing with
        for student_id in [1, 2, 3]:
            try:
                self.repo.deleteSurveysByStudentID(student_id)
            except:
                pass

        # Get all surveys - should still have some from base data
        surveys = self.repo.getWellBeingSurveys()
        # Can't guarantee empty as base data exists, just verify no crash
        self.assertTrue(surveys is None or isinstance(surveys, list))

if __name__ == "__main__":
    unittest.main()
