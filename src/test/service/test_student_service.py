import unittest
from unittest.mock import MagicMock
from base.services.student_service import Student_Service
from base.entity.student import Student
from base.entity.attendance import Attendance
from base.entity.assessments import Assessment
from base.entity.wellbeing_survey import Wellbeing_Survey

class TestStudentService(unittest.TestCase):

    def setUp(self):
        self.student_repo = MagicMock()
        self.attendance_repo = MagicMock()
        self.assessment_repo = MagicMock()
        self.wellbeing_repo = MagicMock()
        
        self.service = Student_Service(
            student_repo=self.student_repo,
            attendance_repo=self.attendance_repo,
            assessment_repo=self.assessment_repo,
            wellbeing_survey_repo=self.wellbeing_repo
        )

    def test_getAllStudent(self):
        self.student_repo.getAllStudent.return_value = [Student(id=1, first_name="Alice", last_name="Brown", email="alice@uni.com", personal_tutor_email="tutor@uni.com", emergency_contact_name="Dad", emergency_contact_phone="07999999999")]
        
        result = self.service.getAllStudent()
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].first_name, "Alice")
        self.student_repo.getAllStudent.assert_called_once()

    def test_getAttdenceByID(self):
        self.attendance_repo.getAttendancesByStudentID.return_value = [Attendance(attendance_id=1, student_id=1, week_number=1, is_present=True, is_late=False)]
        
        result = self.service.getAttdenceByID(1)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].student_id, 1)
        self.attendance_repo.getAttendancesByStudentID.assert_called_once_with(1)

    def test_getAssessmentByID(self):
        self.assessment_repo.getAssessmentsByStudentID.return_value = [Assessment(assessment_id=1, student_id=1, assignment_name="Math", grade=85, submitted_on_time="2024-01-01")]
        
        result = self.service.getAssessmentByID(1)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].student_id, 1)
        self.assessment_repo.getAssessmentsByStudentID.assert_called_once_with(1)

    def test_getWellBeingSurveyByID(self):
        self.wellbeing_repo.getWellBeingSurveysByStudentID.return_value = [Wellbeing_Survey(survey_id=1, student_id=1, week_number=1, stress_level=5, hours_slept=7.0, survey_date="2024-01-01")]
        
        result = self.service.getWellBeingSurveyByID(1)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].student_id, 1)
        self.wellbeing_repo.getWellBeingSurveysByStudentID.assert_called_once_with(1)

    def test_add_student(self):
        student = Student(id=2, first_name="Anna", last_name="Karenina", email="anna@uni.com", personal_tutor_email="tutor@uni.com", emergency_contact_name="Mom", emergency_contact_phone="07123456789")
        self.service.add(student)
        self.student_repo.addStudent.assert_called_once_with(student)

    def test_update_student(self):
        student = Student(id=1, first_name="AliceUpdated", last_name="Brown", email="alice@uni.com", personal_tutor_email="tutor@uni.com", emergency_contact_name="Dad", emergency_contact_phone="07999999999")
        self.service.update(student)
        self.student_repo.updateStudent.assert_called_once_with(student)

    def test_delete_student(self):
        student = Student(id=1, first_name="Alice", last_name="Brown", email="alice@uni.com", personal_tutor_email="tutor@uni.com", emergency_contact_name="Dad", emergency_contact_phone="07999999999")
        self.service.delete(student)
        self.student_repo.deleteStudent.assert_called_once_with(student)


if __name__ == "__main__":
    unittest.main()
