import unittest
from unittest.mock import MagicMock, patch
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

    # ========== Error Propagation Tests ==========

    def test_addWellbeingSurvey_repository_error(self):
        """Test that repository exceptions propagate to service layer"""
        survey = Wellbeing_Survey(
            survey_id=-1,
            student_id=1,
            week_number=5,
            stress_level=3,
            hours_slept=7.5,
            survey_date="2024-01-15"
        )
        self.wellbeing_repo.addWellbeingSurvey.side_effect = Exception("Database error")

        with self.assertRaises(Exception) as context:
            self.service.addWellbeingSurvey(survey)
        self.assertIn("Database error", str(context.exception))

    def test_addAttendance_repository_error(self):
        """Test that repository exceptions propagate to service layer"""
        attendance = Attendance(
            attendance_id=None,
            student_id=1,
            week_number=10,
            is_present=True,
            is_late=False
        )
        self.attendance_repo.addAttendance.side_effect = Exception("Database error")

        with self.assertRaises(Exception) as context:
            self.service.addAttendance(attendance)
        self.assertIn("Database error", str(context.exception))

    def test_addAssessment_repository_error(self):
        """Test that repository exceptions propagate to service layer"""
        assessment = Assessment(
            assessment_id=None,
            student_id=1,
            assignment_name="Test",
            grade=85,
            submitted_on_time=1
        )
        self.assessment_repo.addAssessment.side_effect = Exception("Database error")

        with self.assertRaises(Exception) as context:
            self.service.addAssessment(assessment)
        self.assertIn("Database error", str(context.exception))

    def test_addWellbeingSurvey_validation_error(self):
        """Test that validation errors propagate correctly"""
        survey = Wellbeing_Survey(
            survey_id=-1,
            student_id=1,
            week_number=5,
            stress_level=10,  # Invalid
            hours_slept=7.5,
            survey_date="2024-01-15"
        )
        self.wellbeing_repo.addWellbeingSurvey.side_effect = ValueError("stress_level must be between 1 and 5")

        with self.assertRaises(ValueError) as context:
            self.service.addWellbeingSurvey(survey)
        self.assertIn("stress_level", str(context.exception))

    def test_addAttendance_validation_error(self):
        """Test that validation errors propagate correctly"""
        attendance = Attendance(
            attendance_id=None,
            student_id=1,
            week_number=100,  # Invalid
            is_present=True,
            is_late=False
        )
        self.attendance_repo.addAttendance.side_effect = ValueError("week_number must be between 1 and 52")

        with self.assertRaises(ValueError) as context:
            self.service.addAttendance(attendance)
        self.assertIn("week_number", str(context.exception))

    def test_addAssessment_validation_error(self):
        """Test that validation errors propagate correctly"""
        assessment = Assessment(
            assessment_id=None,
            student_id=1,
            assignment_name="Test",
            grade=150,  # Invalid
            submitted_on_time=1
        )
        self.assessment_repo.addAssessment.side_effect = ValueError("grade must be between 0 and 100")

        with self.assertRaises(ValueError) as context:
            self.service.addAssessment(assessment)
        self.assertIn("grade", str(context.exception))

    # ========== Repository Initialization Tests ==========

    @patch('base.services.user_service.Assessment_Repo')
    @patch('base.services.user_service.Attendance_Repo')
    @patch('base.services.user_service.Wellbeing_Survey_Repo')
    def test_service_initialization_default_repos(self, mock_wellbeing_repo, mock_attendance_repo, mock_assessment_repo):
        """Test service creates default repositories when none provided"""
        service = user_service()
        self.assertIsNotNone(service.wellbeing_survey_repo)
        self.assertIsNotNone(service.attendance_repo)
        self.assertIsNotNone(service.assessment_repo)
        # Verify repository constructors were called
        mock_wellbeing_repo.assert_called_once()
        mock_attendance_repo.assert_called_once()
        mock_assessment_repo.assert_called_once()

    def test_service_initialization_custom_repos(self):
        """Test service accepts custom repositories"""
        custom_wellbeing = MagicMock()
        custom_attendance = MagicMock()
        custom_assessment = MagicMock()

        service = user_service(
            wellbeing_survey_repo=custom_wellbeing,
            attendance_repo=custom_attendance,
            assessment_repo=custom_assessment
        )

        self.assertEqual(service.wellbeing_survey_repo, custom_wellbeing)
        self.assertEqual(service.attendance_repo, custom_attendance)
        self.assertEqual(service.assessment_repo, custom_assessment)

    @patch('base.services.user_service.Assessment_Repo')
    @patch('base.services.user_service.Attendance_Repo')
    def test_service_initialization_partial_repos(self, mock_attendance_repo, mock_assessment_repo):
        """Test service with some custom and some default repos"""
        custom_wellbeing = MagicMock()

        service = user_service(wellbeing_survey_repo=custom_wellbeing)

        self.assertEqual(service.wellbeing_survey_repo, custom_wellbeing)
        self.assertIsNotNone(service.attendance_repo)
        self.assertIsNotNone(service.assessment_repo)
        # Verify only the non-custom repos were created
        mock_attendance_repo.assert_called_once()
        mock_assessment_repo.assert_called_once()

    @patch('base.services.user_service.Assessment_Repo')
    @patch('base.services.user_service.Attendance_Repo')
    @patch('base.services.user_service.Wellbeing_Survey_Repo')
    def test_service_initialization_none_repos(self, mock_wellbeing_repo, mock_attendance_repo, mock_assessment_repo):
        """Test service when explicitly passing None for repos"""
        service = user_service(
            wellbeing_survey_repo=None,
            attendance_repo=None,
            assessment_repo=None
        )

        self.assertIsNotNone(service.wellbeing_survey_repo)
        self.assertIsNotNone(service.attendance_repo)
        self.assertIsNotNone(service.assessment_repo)
        # Verify repository constructors were called
        mock_wellbeing_repo.assert_called_once()
        mock_attendance_repo.assert_called_once()
        mock_assessment_repo.assert_called_once()

    # ========== Multiple Operations Tests ==========

    def test_add_multiple_surveys_same_service(self):
        """Test adding multiple surveys sequentially"""
        surveys = [
            Wellbeing_Survey(-1, 1, 1, 3, 7.5, "2024-01-01"),
            Wellbeing_Survey(-1, 1, 2, 4, 6.5, "2024-01-08"),
            Wellbeing_Survey(-1, 1, 3, 2, 8.0, "2024-01-15")
        ]

        self.wellbeing_repo.addWellbeingSurvey.side_effect = [100, 101, 102]

        results = [self.service.addWellbeingSurvey(survey) for survey in surveys]

        self.assertEqual(results, [100, 101, 102])
        self.assertEqual(self.wellbeing_repo.addWellbeingSurvey.call_count, 3)

    def test_add_multiple_attendances_same_service(self):
        """Test adding multiple attendances sequentially"""
        attendances = [
            Attendance(None, 1, 1, True, False),
            Attendance(None, 1, 2, True, False),
            Attendance(None, 1, 3, False, False)
        ]

        self.attendance_repo.addAttendance.side_effect = [200, 201, 202]

        results = [self.service.addAttendance(attendance) for attendance in attendances]

        self.assertEqual(results, [200, 201, 202])
        self.assertEqual(self.attendance_repo.addAttendance.call_count, 3)

    def test_add_multiple_assessments_same_service(self):
        """Test adding multiple assessments sequentially"""
        assessments = [
            Assessment(None, 1, "Quiz 1", 85, 1),
            Assessment(None, 1, "Quiz 2", 90, 1),
            Assessment(None, 1, "Quiz 3", 88, 0)
        ]

        self.assessment_repo.addAssessment.side_effect = [300, 301, 302]

        results = [self.service.addAssessment(assessment) for assessment in assessments]

        self.assertEqual(results, [300, 301, 302])
        self.assertEqual(self.assessment_repo.addAssessment.call_count, 3)

    def test_mixed_operations(self):
        """Test adding survey, attendance, and assessment in sequence"""
        survey = Wellbeing_Survey(-1, 1, 5, 3, 7.5, "2024-01-15")
        attendance = Attendance(None, 1, 10, True, False)
        assessment = Assessment(None, 1, "Midterm", 85, 1)

        self.wellbeing_repo.addWellbeingSurvey.return_value = 100
        self.attendance_repo.addAttendance.return_value = 200
        self.assessment_repo.addAssessment.return_value = 300

        survey_result = self.service.addWellbeingSurvey(survey)
        attendance_result = self.service.addAttendance(attendance)
        assessment_result = self.service.addAssessment(assessment)

        self.assertEqual(survey_result, 100)
        self.assertEqual(attendance_result, 200)
        self.assertEqual(assessment_result, 300)

        self.wellbeing_repo.addWellbeingSurvey.assert_called_once_with(survey)
        self.attendance_repo.addAttendance.assert_called_once_with(attendance)
        self.assessment_repo.addAssessment.assert_called_once_with(assessment)

    # ========== Return Value Verification Tests ==========

    def test_addWellbeingSurvey_return_type(self):
        """Verify return type is int"""
        survey = Wellbeing_Survey(-1, 1, 5, 3, 7.5, "2024-01-15")
        self.wellbeing_repo.addWellbeingSurvey.return_value = 100

        result = self.service.addWellbeingSurvey(survey)

        self.assertIsInstance(result, int)

    def test_addAttendance_return_type(self):
        """Verify return type is int"""
        attendance = Attendance(None, 1, 10, True, False)
        self.attendance_repo.addAttendance.return_value = 200

        result = self.service.addAttendance(attendance)

        self.assertIsInstance(result, int)

    def test_addAssessment_return_type(self):
        """Verify return type is int"""
        assessment = Assessment(None, 1, "Test", 85, 1)
        self.assessment_repo.addAssessment.return_value = 300

        result = self.service.addAssessment(assessment)

        self.assertIsInstance(result, int)

    def test_operations_return_positive_ids(self):
        """Verify all operations return positive IDs"""
        survey = Wellbeing_Survey(-1, 1, 5, 3, 7.5, "2024-01-15")
        attendance = Attendance(None, 1, 10, True, False)
        assessment = Assessment(None, 1, "Test", 85, 1)

        self.wellbeing_repo.addWellbeingSurvey.return_value = 100
        self.attendance_repo.addAttendance.return_value = 200
        self.assessment_repo.addAssessment.return_value = 300

        survey_result = self.service.addWellbeingSurvey(survey)
        attendance_result = self.service.addAttendance(attendance)
        assessment_result = self.service.addAssessment(assessment)

        self.assertGreater(survey_result, 0)
        self.assertGreater(attendance_result, 0)
        self.assertGreater(assessment_result, 0)

    # ========== Edge Cases Tests ==========

    def test_service_method_called_once(self):
        """Verify repository method called exactly once"""
        survey = Wellbeing_Survey(-1, 1, 5, 3, 7.5, "2024-01-15")
        self.wellbeing_repo.addWellbeingSurvey.return_value = 100

        self.service.addWellbeingSurvey(survey)

        self.wellbeing_repo.addWellbeingSurvey.assert_called_once()

    def test_service_delegates_correctly(self):
        """Verify service correctly delegates to repositories"""
        survey = Wellbeing_Survey(-1, 1, 5, 3, 7.5, "2024-01-15")
        attendance = Attendance(None, 1, 10, True, False)
        assessment = Assessment(None, 1, "Test", 85, 1)

        self.wellbeing_repo.addWellbeingSurvey.return_value = 100
        self.attendance_repo.addAttendance.return_value = 200
        self.assessment_repo.addAssessment.return_value = 300

        # Call service methods
        self.service.addWellbeingSurvey(survey)
        self.service.addAttendance(attendance)
        self.service.addAssessment(assessment)

        # Verify correct repository methods were called with correct arguments
        self.wellbeing_repo.addWellbeingSurvey.assert_called_once_with(survey)
        self.attendance_repo.addAttendance.assert_called_once_with(attendance)
        self.assessment_repo.addAssessment.assert_called_once_with(assessment)

        # Verify other repository methods were NOT called
        self.assertEqual(self.wellbeing_repo.addWellbeingSurvey.call_count, 1)
        self.assertEqual(self.attendance_repo.addAttendance.call_count, 1)
        self.assertEqual(self.assessment_repo.addAssessment.call_count, 1)


if __name__ == "__main__":
    unittest.main()
