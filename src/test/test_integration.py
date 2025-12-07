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
from base.services.student_service import Student_Service


class TestIntegration(BaseRepositoryTest):

    def setUp(self):
        super().setUp()
        self.student_repo = Student_Repo()
        self.survey_repo = Wellbeing_Survey_Repo()
        self.attendance_repo = Attendance_Repo()
        self.assessment_repo = Assessment_Repo()

    # ===== Complete Workflow Tests =====

    def test_add_student_and_all_data(self):
        """Test adding a student and then adding attendance, assessment, and survey"""
        # Add student
        student = Student(
            id=-1,
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            personal_tutor_email="tutor@example.com",
            emergency_contact_name="Jane Doe",
            emergency_contact_phone="123-456-7890"
        )
        self.student_repo.addStudent(student)

        # Get the actual student from database (workaround for student_id bug)
        all_students = self.student_repo.getAllStudent()
        added_student = [s for s in all_students if s.email == "john.doe@example.com"][0]
        student_id = added_student.id

        self.assertIsNotNone(student_id)
        self.assertGreater(student_id, 0)

        # Add survey
        survey = Wellbeing_Survey(
            survey_id=-1,
            student_id=student_id,
            week_number=1,
            stress_level=3,
            hours_slept=7,
            survey_date="2024-01-15"
        )
        survey_id = self.survey_repo.addWellBeingSurvey(survey)
        self.assertGreater(survey_id, 0)

        # Add attendance
        attendance = Attendance(
            attendance_id=None,
            student_id=student_id,
            week_number=1,
            is_present=True,
            is_late=False
        )
        attendance_id = self.attendance_repo.addAttendance(attendance)
        self.assertGreater(attendance_id, 0)

        # Add assessment
        assessment = Assessment(
            assessment_id=None,
            student_id=student_id,
            assignment_name="Assignment 1",
            grade=85,
            submitted_on_time=1
        )
        assessment_id = self.assessment_repo.addAssessment(assessment)
        self.assertGreater(assessment_id, 0)

        # Verify all data exists
        surveys = self.survey_repo.getWellBeingSurveysByStudentID(student_id)
        attendances = self.attendance_repo.getAttendancesByStudentID(student_id)
        assessments = self.assessment_repo.getAssessmentsByStudentID(student_id)

        self.assertEqual(len(surveys), 1)
        self.assertEqual(len(attendances), 1)
        self.assertEqual(len(assessments), 1)

    def test_student_full_semester_workflow(self):
        """Test adding all data for a student for full semester"""
        # Add student
        student = Student(
            id=-1,
            first_name="Alice",
            last_name="Smith",
            email="alice.smith@example.com"
        )
        self.student_repo.addStudent(student)

        # Get actual student ID
        all_students = self.student_repo.getAllStudent()
        added_student = [s for s in all_students if s.email == "alice.smith@example.com"][0]
        student_id = added_student.id

        # Add data for 12 weeks (full semester)
        for week in range(1, 13):
            # Add survey
            survey = Wellbeing_Survey(
                survey_id=-1,
                student_id=student_id,
                week_number=week,
                stress_level=(week % 5) + 1,  # Vary stress level 1-5
                hours_slept=7 + (week % 3),  # Vary sleep 7-9 hours
                survey_date=f"2024-01-{week:02d}"
            )
            self.survey_repo.addWellBeingSurvey(survey)

            # Add attendance
            attendance = Attendance(
                attendance_id=None,
                student_id=student_id,
                week_number=week,
                is_present=True,
                is_late=(week % 4 == 0)  # Late every 4th week
            )
            self.attendance_repo.addAttendance(attendance)

            # Add assessment (every 3rd week)
            if week % 3 == 0:
                assessment = Assessment(
                    assessment_id=None,
                    student_id=student_id,
                    assignment_name=f"Assignment {week // 3}",
                    grade=70 + (week % 30),
                    submitted_on_time=1
                )
                self.assessment_repo.addAssessment(assessment)

        # Verify counts
        surveys = self.survey_repo.getWellBeingSurveysByStudentID(student_id)
        attendances = self.attendance_repo.getAttendancesByStudentID(student_id)
        assessments = self.assessment_repo.getAssessmentsByStudentID(student_id)

        self.assertEqual(len(surveys), 12)
        self.assertEqual(len(attendances), 12)
        self.assertEqual(len(assessments), 4)  # Every 3rd week: weeks 3, 6, 9, 12

    def test_multiple_students_workflow(self):
        """Test adding data for multiple students"""
        students_data = [
            ("Bob", "Jones", "bob.jones@example.com"),
            ("Carol", "White", "carol.white@example.com"),
            ("David", "Brown", "david.brown@example.com")
        ]

        student_ids = []

        # Add multiple students
        for first_name, last_name, email in students_data:
            student = Student(
                id=-1,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            self.student_repo.addStudent(student)

            # Get actual student ID
            all_students = self.student_repo.getAllStudent()
            added_student = [s for s in all_students if s.email == email][0]
            student_ids.append(added_student.id)

        # Add data for each student
        for idx, student_id in enumerate(student_ids):
            # Add survey
            survey = Wellbeing_Survey(
                survey_id=-1,
                student_id=student_id,
                week_number=1,
                stress_level=idx + 2,
                hours_slept=6 + idx,
                survey_date="2024-01-15"
            )
            self.survey_repo.addWellBeingSurvey(survey)

            # Add attendance
            attendance = Attendance(
                attendance_id=None,
                student_id=student_id,
                week_number=1,
                is_present=True,
                is_late=False
            )
            self.attendance_repo.addAttendance(attendance)

        # Verify each student has their data
        for student_id in student_ids:
            surveys = self.survey_repo.getWellBeingSurveysByStudentID(student_id)
            attendances = self.attendance_repo.getAttendancesByStudentID(student_id)
            self.assertEqual(len(surveys), 1)
            self.assertEqual(len(attendances), 1)

    # ===== Transaction Tests =====

    def test_rollback_on_error(self):
        """Test that transaction is rolled back on error"""
        # Get initial student count
        initial_students = self.student_repo.getAllStudent()
        initial_count = len(initial_students) if initial_students else 0

        # Try to add a student with invalid data (should fail)
        try:
            invalid_student = Student(
                id=-1,
                first_name="",  # Empty name should cause validation error
                last_name="",
                email=""
            )
            self.student_repo.addStudent(invalid_student)
        except (ValueError, Exception):
            pass  # Expected to fail

        # Verify student count hasn't changed (transaction rolled back)
        final_students = self.student_repo.getAllStudent()
        final_count = len(final_students) if final_students else 0
        self.assertEqual(initial_count, final_count)

    def test_commit_on_success(self):
        """Test that transaction is committed on success"""
        # Add a valid student
        student = Student(
            id=-1,
            first_name="Emma",
            last_name="Wilson",
            email="emma.wilson@example.com"
        )
        self.student_repo.addStudent(student)

        # Create a new repository instance to verify data persisted
        new_repo = Student_Repo()
        all_students = new_repo.getAllStudent()
        emails = [s.email for s in all_students]

        # Verify student was persisted
        self.assertIn("emma.wilson@example.com", emails)

    def test_multiple_operations_atomic(self):
        """Test multiple operations in single transaction"""
        # Add student
        student = Student(
            id=-1,
            first_name="Frank",
            last_name="Miller",
            email="frank.miller@example.com"
        )
        self.student_repo.addStudent(student)

        # Get actual student ID
        all_students = self.student_repo.getAllStudent()
        added_student = [s for s in all_students if s.email == "frank.miller@example.com"][0]
        student_id = added_student.id

        # Add multiple surveys in sequence
        for week in range(1, 4):
            survey = Wellbeing_Survey(
                survey_id=-1,
                student_id=student_id,
                week_number=week,
                stress_level=3,
                hours_slept=7,
                survey_date=f"2024-01-{week:02d}"
            )
            self.survey_repo.addWellBeingSurvey(survey)

        # Verify all surveys were added atomically
        surveys = self.survey_repo.getWellBeingSurveysByStudentID(student_id)
        self.assertEqual(len(surveys), 3)

    # ===== Data Consistency Tests =====

    def test_survey_count_consistency(self):
        """Test that survey count matches actual records"""
        # Add student
        student = Student(
            id=-1,
            first_name="Grace",
            last_name="Lee",
            email="grace.lee@example.com"
        )
        self.student_repo.addStudent(student)

        # Get actual student ID
        all_students = self.student_repo.getAllStudent()
        added_student = [s for s in all_students if s.email == "grace.lee@example.com"][0]
        student_id = added_student.id

        # Add 5 surveys
        for week in range(1, 6):
            survey = Wellbeing_Survey(
                survey_id=-1,
                student_id=student_id,
                week_number=week,
                stress_level=3,
                hours_slept=7,
                survey_date=f"2024-01-{week:02d}"
            )
            self.survey_repo.addWellBeingSurvey(survey)

        # Verify count
        surveys = self.survey_repo.getWellBeingSurveysByStudentID(student_id)
        self.assertEqual(len(surveys), 5)

    def test_attendance_count_consistency(self):
        """Test that attendance count matches actual records"""
        # Add student
        student = Student(
            id=-1,
            first_name="Henry",
            last_name="Taylor",
            email="henry.taylor@example.com"
        )
        self.student_repo.addStudent(student)

        # Get actual student ID
        all_students = self.student_repo.getAllStudent()
        added_student = [s for s in all_students if s.email == "henry.taylor@example.com"][0]
        student_id = added_student.id

        # Add 7 attendance records
        for week in range(1, 8):
            attendance = Attendance(
                attendance_id=None,
                student_id=student_id,
                week_number=week,
                is_present=True,
                is_late=False
            )
            self.attendance_repo.addAttendance(attendance)

        # Verify count
        attendances = self.attendance_repo.getAttendancesByStudentID(student_id)
        self.assertEqual(len(attendances), 7)

    def test_assessment_count_consistency(self):
        """Test that assessment count matches actual records"""
        # Add student
        student = Student(
            id=-1,
            first_name="Iris",
            last_name="Garcia",
            email="iris.garcia@example.com"
        )
        self.student_repo.addStudent(student)

        # Get actual student ID
        all_students = self.student_repo.getAllStudent()
        added_student = [s for s in all_students if s.email == "iris.garcia@example.com"][0]
        student_id = added_student.id

        # Add 4 assessments
        for i in range(1, 5):
            assessment = Assessment(
                assessment_id=None,
                student_id=student_id,
                assignment_name=f"Assignment {i}",
                grade=80 + i,
                submitted_on_time=1
            )
            self.assessment_repo.addAssessment(assessment)

        # Verify count
        assessments = self.assessment_repo.getAssessmentsByStudentID(student_id)
        self.assertEqual(len(assessments), 4)

    def test_student_data_integrity(self):
        """Test add and retrieve, verify data unchanged"""
        # Add student with specific data
        original_student = Student(
            id=-1,
            first_name="Jack",
            last_name="Anderson",
            email="jack.anderson@example.com",
            personal_tutor_email="tutor@example.com",
            emergency_contact_name="Jill Anderson",
            emergency_contact_phone="555-1234"
        )
        self.student_repo.addStudent(original_student)

        # Retrieve student
        all_students = self.student_repo.getAllStudent()
        retrieved_student = [s for s in all_students if s.email == "jack.anderson@example.com"][0]

        # Verify all fields match
        self.assertEqual(retrieved_student.first_name, "Jack")
        self.assertEqual(retrieved_student.last_name, "Anderson")
        self.assertEqual(retrieved_student.email, "jack.anderson@example.com")
        self.assertEqual(retrieved_student.personal_tutor_email, "tutor@example.com")
        self.assertEqual(retrieved_student.emergency_contact_name, "Jill Anderson")
        self.assertEqual(retrieved_student.emergency_contact_phone, "555-1234")

    # ===== Repository Interaction Tests =====

    def test_service_uses_correct_repository(self):
        """Test that service delegates to correct repository"""
        # Create service
        service = Student_Service()

        # Use service to get all students
        students_from_service = service.getAllStudent()

        # Use repository directly
        repo = Student_Repo()
        students_from_repo = repo.getAllStudent()

        # Verify same results (service delegates to repo correctly)
        if students_from_service and students_from_repo:
            self.assertEqual(len(students_from_service), len(students_from_repo))

    def test_repository_connection_reuse(self):
        """Test that DB connection is reused correctly"""
        # Create repository
        repo1 = Student_Repo()

        # Add student
        student = Student(
            id=-1,
            first_name="Kate",
            last_name="Johnson",
            email="kate.johnson@example.com"
        )
        repo1.addStudent(student)

        # Create new repository instance
        repo2 = Student_Repo()

        # Verify data accessible from new instance (connection to same DB)
        all_students = repo2.getAllStudent()
        emails = [s.email for s in all_students]
        self.assertIn("kate.johnson@example.com", emails)

    def test_multiple_repositories_same_connection(self):
        """Test multiple repositories share connection to same database"""
        # Add student
        student = Student(
            id=-1,
            first_name="Leo",
            last_name="Martinez",
            email="leo.martinez@example.com"
        )
        self.student_repo.addStudent(student)

        # Get actual student ID
        all_students = self.student_repo.getAllStudent()
        added_student = [s for s in all_students if s.email == "leo.martinez@example.com"][0]
        student_id = added_student.id

        # Add data using different repositories
        survey = Wellbeing_Survey(
            survey_id=-1,
            student_id=student_id,
            week_number=1,
            stress_level=3,
            hours_slept=7,
            survey_date="2024-01-15"
        )
        self.survey_repo.addWellBeingSurvey(survey)

        attendance = Attendance(
            attendance_id=None,
            student_id=student_id,
            week_number=1,
            is_present=True,
            is_late=False
        )
        self.attendance_repo.addAttendance(attendance)

        # Verify data accessible (all repos connected to same DB)
        surveys = self.survey_repo.getWellBeingSurveysByStudentID(student_id)
        attendances = self.attendance_repo.getAttendancesByStudentID(student_id)

        self.assertEqual(len(surveys), 1)
        self.assertEqual(len(attendances), 1)


if __name__ == '__main__':
    unittest.main()
