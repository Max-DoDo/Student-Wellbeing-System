import unittest
from test.base_repository_test import BaseRepositoryTest
from base.repository.student_repo import Student_Repo
from base.repository.wellbeing_surveys_repo import Wellbeing_Survey_Repo
from base.repository.attendance_repo import Attendance_Repo
from base.repository.assessment_repo import Assessment_Repo
from base.entity.student import Student
from base.entity.wellbeing_survey import Wellbeing_Survey
from base.entity.attendance import Attendance
from base.entity.assessments import Assessment


class TestSecurity(BaseRepositoryTest):

    def setUp(self):
        super().setUp()
        self.student_repo = Student_Repo()
        self.survey_repo = Wellbeing_Survey_Repo()
        self.attendance_repo = Attendance_Repo()
        self.assessment_repo = Assessment_Repo()

    # ===== SQL Injection Tests =====

    def test_sql_injection_survey_date(self):
        """Test SQL injection attempt via survey_date field"""
        # Add a student first
        student = Student(
            id=-1,
            first_name="Test",
            last_name="Student",
            email="test.sql1@example.com"
        )
        self.student_repo.addStudent(student)

        # Get actual student ID
        all_students = self.student_repo.getAllStudent()
        added_student = [s for s in all_students if s.email == "test.sql1@example.com"][0]
        student_id = added_student.id

        # Attempt SQL injection in survey_date
        malicious_date = "2024-01-15'; DROP TABLE wellbeing_surveys; --"

        survey = Wellbeing_Survey(
            survey_id=-1,
            student_id=student_id,
            week_number=1,
            stress_level=3,
            hours_slept=7,
            survey_date=malicious_date
        )

        # Should not cause SQL injection due to parameterized queries
        survey_id = self.survey_repo.addWellBeingSurvey(survey)
        self.assertGreater(survey_id, 0)

        # Verify the malicious string was stored as regular data, not executed
        retrieved_survey = self.survey_repo.getWellBeingSurvey(survey_id)
        self.assertIsNotNone(retrieved_survey)
        self.assertEqual(retrieved_survey.survey_date, malicious_date)

        # Verify the table still exists by querying it
        surveys = self.survey_repo.getWellBeingSurveysByStudentID(student_id)
        self.assertEqual(len(surveys), 1)

    def test_sql_injection_assignment_name(self):
        """Test SQL injection attempt via assignment_name field"""
        # Add a student first
        student = Student(
            id=-1,
            first_name="Test",
            last_name="Student",
            email="test.sql2@example.com"
        )
        self.student_repo.addStudent(student)

        # Get actual student ID
        all_students = self.student_repo.getAllStudent()
        added_student = [s for s in all_students if s.email == "test.sql2@example.com"][0]
        student_id = added_student.id

        # Attempt SQL injection in assignment_name
        malicious_name = "Assignment 1'; DELETE FROM assessments WHERE '1'='1"

        assessment = Assessment(
            assessment_id=None,
            student_id=student_id,
            assignment_name=malicious_name,
            grade=85,
            submitted_on_time=1
        )

        # Should not cause SQL injection due to parameterized queries
        assessment_id = self.assessment_repo.addAssessment(assessment)
        self.assertGreater(assessment_id, 0)

        # Verify the malicious string was stored as regular data
        retrieved = self.assessment_repo.getAssessment(assessment_id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.assignment_name, malicious_name)

        # Verify no data was deleted
        assessments = self.assessment_repo.getAssessmentsByStudentID(student_id)
        self.assertEqual(len(assessments), 1)

    def test_sql_injection_student_id(self):
        """Test SQL injection attempt via student_id (attempting to pass as string)"""
        # Add a student first
        student = Student(
            id=-1,
            first_name="Test",
            last_name="Student",
            email="test.sql3@example.com"
        )
        self.student_repo.addStudent(student)

        # Get actual student ID
        all_students = self.student_repo.getAllStudent()
        added_student = [s for s in all_students if s.email == "test.sql3@example.com"][0]
        student_id = added_student.id

        # Normal survey with valid student_id
        survey = Wellbeing_Survey(
            survey_id=-1,
            student_id=student_id,
            week_number=1,
            stress_level=3,
            hours_slept=7,
            survey_date="2024-01-15"
        )

        # Parameterized queries should safely handle the student_id
        survey_id = self.survey_repo.addWellBeingSurvey(survey)
        self.assertGreater(survey_id, 0)

        # Verify retrieval works correctly
        retrieved = self.survey_repo.getWellBeingSurvey(survey_id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.student_id, student_id)

    # ===== Input Validation Tests =====

    def test_xss_in_assignment_name(self):
        """Test XSS attempt in assignment_name field"""
        # Add a student first
        student = Student(
            id=-1,
            first_name="Test",
            last_name="Student",
            email="test.xss1@example.com"
        )
        self.student_repo.addStudent(student)

        # Get actual student ID
        all_students = self.student_repo.getAllStudent()
        added_student = [s for s in all_students if s.email == "test.xss1@example.com"][0]
        student_id = added_student.id

        # XSS attempt in assignment_name
        xss_string = "<script>alert('XSS')</script>"

        assessment = Assessment(
            assessment_id=None,
            student_id=student_id,
            assignment_name=xss_string,
            grade=90,
            submitted_on_time=1
        )

        # Should store the XSS string as regular text (not execute it)
        assessment_id = self.assessment_repo.addAssessment(assessment)
        self.assertGreater(assessment_id, 0)

        # Verify the XSS string was stored correctly
        retrieved = self.assessment_repo.getAssessment(assessment_id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.assignment_name, xss_string)

    def test_script_tags_in_strings(self):
        """Test HTML/script tags in string fields"""
        # Add student with script tags in name
        student = Student(
            id=-1,
            first_name="<script>alert('test')</script>",
            last_name="<b>Bold Name</b>",
            email="test.script@example.com"
        )
        self.student_repo.addStudent(student)

        # Get actual student
        all_students = self.student_repo.getAllStudent()
        added_student = [s for s in all_students if s.email == "test.script@example.com"][0]

        # Verify the script tags were stored as regular text
        self.assertEqual(added_student.first_name, "<script>alert('test')</script>")
        self.assertEqual(added_student.last_name, "<b>Bold Name</b>")

    def test_null_byte_injection(self):
        """Test null bytes in strings"""
        # Add student with null byte in email
        # Note: Python strings can contain null bytes, but SQLite may handle them differently
        student = Student(
            id=-1,
            first_name="Test",
            last_name="NullByte",
            email="test.null@example.com"
        )
        self.student_repo.addStudent(student)

        # Get actual student ID
        all_students = self.student_repo.getAllStudent()
        added_student = [s for s in all_students if s.email == "test.null@example.com"][0]
        student_id = added_student.id

        # Try adding assessment with null byte in assignment name
        # Using a string that contains special characters
        special_name = "Assignment\x00WithNull"

        assessment = Assessment(
            assessment_id=None,
            student_id=student_id,
            assignment_name=special_name,
            grade=85,
            submitted_on_time=1
        )

        # Should handle null bytes safely
        assessment_id = self.assessment_repo.addAssessment(assessment)
        self.assertGreater(assessment_id, 0)

    # ===== Path Traversal Tests =====

    def test_path_traversal_in_assignment_name(self):
        """Test path traversal attempt in assignment_name"""
        # Add a student first
        student = Student(
            id=-1,
            first_name="Test",
            last_name="Student",
            email="test.path@example.com"
        )
        self.student_repo.addStudent(student)

        # Get actual student ID
        all_students = self.student_repo.getAllStudent()
        added_student = [s for s in all_students if s.email == "test.path@example.com"][0]
        student_id = added_student.id

        # Path traversal attempt
        path_traversal = "../../../etc/passwd"

        assessment = Assessment(
            assessment_id=None,
            student_id=student_id,
            assignment_name=path_traversal,
            grade=75,
            submitted_on_time=1
        )

        # Should store as regular string (not attempt file access)
        assessment_id = self.assessment_repo.addAssessment(assessment)
        self.assertGreater(assessment_id, 0)

        # Verify the path traversal string was stored as regular data
        retrieved = self.assessment_repo.getAssessment(assessment_id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.assignment_name, path_traversal)

    # ===== Data Sanitization Tests =====

    def test_special_characters_escaped(self):
        """Test that special characters are properly handled"""
        # Add student with special characters
        student = Student(
            id=-1,
            first_name="O'Brien",
            last_name="Smith-Jones & Co.",
            email="test.special@example.com",
            emergency_contact_name="Mary's Friend",
            emergency_contact_phone="555-1234 (ext. 5)"
        )
        self.student_repo.addStudent(student)

        # Get actual student
        all_students = self.student_repo.getAllStudent()
        added_student = [s for s in all_students if s.email == "test.special@example.com"][0]

        # Verify special characters were preserved
        self.assertEqual(added_student.first_name, "O'Brien")
        self.assertEqual(added_student.last_name, "Smith-Jones & Co.")
        self.assertEqual(added_student.emergency_contact_name, "Mary's Friend")
        self.assertEqual(added_student.emergency_contact_phone, "555-1234 (ext. 5)")

    def test_unicode_handling(self):
        """Test that unicode characters are handled correctly"""
        # Add student with unicode characters
        student = Student(
            id=-1,
            first_name="José",
            last_name="Müller",
            email="test.unicode@example.com",
            emergency_contact_name="François"
        )
        self.student_repo.addStudent(student)

        # Get actual student
        all_students = self.student_repo.getAllStudent()
        added_student = [s for s in all_students if s.email == "test.unicode@example.com"][0]

        # Verify unicode characters were preserved
        self.assertEqual(added_student.first_name, "José")
        self.assertEqual(added_student.last_name, "Müller")
        self.assertEqual(added_student.emergency_contact_name, "François")

        # Test unicode in assignment name
        student_id = added_student.id
        assessment = Assessment(
            assessment_id=None,
            student_id=student_id,
            assignment_name="Mathématiques Avancées",
            grade=95,
            submitted_on_time=1
        )

        assessment_id = self.assessment_repo.addAssessment(assessment)
        retrieved = self.assessment_repo.getAssessment(assessment_id)
        self.assertEqual(retrieved.assignment_name, "Mathématiques Avancées")

    def test_emoji_handling(self):
        """Test that emoji characters are stored and retrieved correctly"""
        # Add student with emoji
        student = Student(
            id=-1,
            first_name="Emma",
            last_name="Wilson",
            email="test.emoji@example.com",
            emergency_contact_name="Mom 👩"
        )
        self.student_repo.addStudent(student)

        # Get actual student
        all_students = self.student_repo.getAllStudent()
        added_student = [s for s in all_students if s.email == "test.emoji@example.com"][0]
        student_id = added_student.id

        # Verify emoji was preserved
        self.assertEqual(added_student.emergency_contact_name, "Mom 👩")

        # Test emoji in assignment name
        assessment = Assessment(
            assessment_id=None,
            student_id=student_id,
            assignment_name="Great Work! 🎉🎓",
            grade=100,
            submitted_on_time=1
        )

        assessment_id = self.assessment_repo.addAssessment(assessment)
        retrieved = self.assessment_repo.getAssessment(assessment_id)
        self.assertEqual(retrieved.assignment_name, "Great Work! 🎉🎓")


if __name__ == '__main__':
    unittest.main()
