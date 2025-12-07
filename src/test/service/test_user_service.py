import unittest
from unittest.mock import MagicMock
from base.services.user_service import user_service
from base.entity.wellbeing_survey import Wellbeing_Survey
from base.entity.attendance import Attendance
from base.entity.assessments import Assessment

class TestUserService(unittest.TestCase):

    def setUp(self):
        self.wellbeing_repo = MagicMock()
        self.attendance_repo = MagicMock()
        self.assessment_repo = MagicMock()
        self.service = user_service(
            wellbeing_survey_repo=self.wellbeing_repo,
            attendance_repo=self.attendance_repo,
            assessment_repo=self.assessment_repo
        )

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

    def test_addAttendance_success(self):
        attendance = Attendance(
            attendance_id=None,
            student_id=1,
            week_number=10,
            is_present=True,
            is_late=False
        )
        self.attendance_repo.addAttendance.return_value = 200

        result = self.service.addAttendance(attendance)

        self.assertEqual(result, 200)
        self.attendance_repo.addAttendance.assert_called_once_with(attendance)

    def test_addAttendance_present_and_late(self):
        attendance = Attendance(
            attendance_id=None,
            student_id=2,
            week_number=5,
            is_present=True,
            is_late=True
        )
        self.attendance_repo.addAttendance.return_value = 201

        result = self.service.addAttendance(attendance)

        self.assertEqual(result, 201)
        self.attendance_repo.addAttendance.assert_called_once_with(attendance)

    def test_addAttendance_absent(self):
        attendance = Attendance(
            attendance_id=None,
            student_id=3,
            week_number=8,
            is_present=False,
            is_late=False
        )
        self.attendance_repo.addAttendance.return_value = 202

        result = self.service.addAttendance(attendance)

        self.assertEqual(result, 202)
        self.attendance_repo.addAttendance.assert_called_once_with(attendance)

    def test_addAssessment_success(self):
        assessment = Assessment(
            assessment_id=None,
            student_id=1,
            assignment_name="Midterm Exam",
            grade=85,
            submitted_on_time=1
        )
        self.assessment_repo.addAssessment.return_value = 300

        result = self.service.addAssessment(assessment)

        self.assertEqual(result, 300)
        self.assessment_repo.addAssessment.assert_called_once_with(assessment)

    def test_addAssessment_perfect_score(self):
        assessment = Assessment(
            assessment_id=None,
            student_id=2,
            assignment_name="Final Project",
            grade=100,
            submitted_on_time=1
        )
        self.assessment_repo.addAssessment.return_value = 301

        result = self.service.addAssessment(assessment)

        self.assertEqual(result, 301)
        self.assessment_repo.addAssessment.assert_called_once_with(assessment)

    def test_addAssessment_submitted_late(self):
        assessment = Assessment(
            assessment_id=None,
            student_id=3,
            assignment_name="Late Homework",
            grade=70,
            submitted_on_time=0
        )
        self.assessment_repo.addAssessment.return_value = 302

        result = self.service.addAssessment(assessment)

        self.assertEqual(result, 302)
        self.assessment_repo.addAssessment.assert_called_once_with(assessment)


if __name__ == "__main__":
    unittest.main()
