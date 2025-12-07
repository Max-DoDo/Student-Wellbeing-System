import unittest
from base.repository.assessment_repo import Assessment_Repo
from base.entity.assessments import Assessment
from test.base_repository_test import BaseRepositoryTest

class TestAssessmentRepo(BaseRepositoryTest):

    def setUp(self):
        self.repo = Assessment_Repo()

    def test_getAssessment_not_found(self):
        """Test fetching an ID that does not exist returns None."""
        a = self.repo.getAssessment(9999) # Use a high number to ensure not found
        self.assertIsNone(a)

    def test_getAssessments(self):
        """Test fetching all assessments returns list with correct items."""
        items = self.repo.getAssessments()
        self.assertIsInstance(items, list)
        self.assertGreater(len(items), 0) # Assuming there's at least one assessment

    def test_addAssessment_auto_id(self):
        assessment = Assessment(
            assessment_id=None,
            student_id=1,
            assignment_name="Final Exam",
            grade=92,
            submitted_on_time=1
        )
        assessment_id = self.repo.addAssessment(assessment)
        self.assertIsNotNone(assessment_id)
        self.assertGreater(assessment_id, 0)

        # Verify the assessment was added
        added_assessment = self.repo.getAssessment(assessment_id)
        self.assertIsNotNone(added_assessment)
        self.assertEqual(added_assessment.student_id, 1)
        self.assertEqual(added_assessment.assignment_name, "Final Exam")
        self.assertEqual(added_assessment.grade, 92)
        self.assertEqual(added_assessment.submitted_on_time, 1)

    def test_addAssessment_submitted_late(self):
        assessment = Assessment(
            assessment_id=None,
            student_id=2,
            assignment_name="Late Assignment",
            grade=75,
            submitted_on_time=0
        )
        assessment_id = self.repo.addAssessment(assessment)
        self.assertIsNotNone(assessment_id)

        added_assessment = self.repo.getAssessment(assessment_id)
        self.assertEqual(added_assessment.submitted_on_time, 0)
        self.assertEqual(added_assessment.grade, 75)

    def test_addAssessment_missing_student_id(self):
        assessment = Assessment(
            assessment_id=None,
            student_id=None,
            assignment_name="Test",
            grade=80,
            submitted_on_time=1
        )
        with self.assertRaises(ValueError) as context:
            self.repo.addAssessment(assessment)
        self.assertIn("Missing required assessment fields", str(context.exception))

    def test_addAssessment_missing_assignment_name(self):
        assessment = Assessment(
            assessment_id=None,
            student_id=1,
            assignment_name=None,
            grade=80,
            submitted_on_time=1
        )
        with self.assertRaises(ValueError) as context:
            self.repo.addAssessment(assessment)
        self.assertIn("Missing required assessment fields", str(context.exception))

    def test_addAssessment_missing_grade(self):
        assessment = Assessment(
            assessment_id=None,
            student_id=1,
            assignment_name="Test",
            grade=None,
            submitted_on_time=1
        )
        with self.assertRaises(ValueError) as context:
            self.repo.addAssessment(assessment)
        self.assertIn("Missing required assessment fields", str(context.exception))

    def test_addAssessment_missing_submitted_on_time(self):
        assessment = Assessment(
            assessment_id=None,
            student_id=1,
            assignment_name="Test",
            grade=80,
            submitted_on_time=""
        )
        with self.assertRaises(ValueError) as context:
            self.repo.addAssessment(assessment)
        self.assertIn("Missing required assessment fields", str(context.exception))

    def test_addAssessment_boundary_grade_min(self):
        assessment = Assessment(
            assessment_id=None,
            student_id=1,
            assignment_name="Poor Assignment",
            grade=0,
            submitted_on_time=1
        )
        assessment_id = self.repo.addAssessment(assessment)
        self.assertIsNotNone(assessment_id)

        added_assessment = self.repo.getAssessment(assessment_id)
        self.assertEqual(added_assessment.grade, 0)

    def test_addAssessment_boundary_grade_max(self):
        assessment = Assessment(
            assessment_id=None,
            student_id=1,
            assignment_name="Perfect Assignment",
            grade=100,
            submitted_on_time=1
        )
        assessment_id = self.repo.addAssessment(assessment)
        self.assertIsNotNone(assessment_id)

        added_assessment = self.repo.getAssessment(assessment_id)
        self.assertEqual(added_assessment.grade, 100)

    def test_addAssessment_various_assignment_names(self):
        assignments = [
            ("Midterm Exam", 85),
            ("Group Project", 90),
            ("Lab Report", 88)
        ]

        for name, grade in assignments:
            assessment = Assessment(
                assessment_id=None,
                student_id=1,
                assignment_name=name,
                grade=grade,
                submitted_on_time=1
            )
            assessment_id = self.repo.addAssessment(assessment)
            self.assertIsNotNone(assessment_id)

            added_assessment = self.repo.getAssessment(assessment_id)
            self.assertEqual(added_assessment.assignment_name, name)
            self.assertEqual(added_assessment.grade, grade)

    # ========== Invalid Boundary Values Tests ==========

    def test_addAssessment_grade_negative(self):
        assessment = Assessment(
            assessment_id=None,
            student_id=1,
            assignment_name="Test",
            grade=-1,
            submitted_on_time=1
        )
        with self.assertRaises(ValueError):
            self.repo.addAssessment(assessment)

    def test_addAssessment_grade_above_max(self):
        assessment = Assessment(
            assessment_id=None,
            student_id=1,
            assignment_name="Test",
            grade=101,
            submitted_on_time=1
        )
        with self.assertRaises(ValueError):
            self.repo.addAssessment(assessment)

    def test_addAssessment_grade_very_large(self):
        assessment = Assessment(
            assessment_id=None,
            student_id=1,
            assignment_name="Test",
            grade=1000000,
            submitted_on_time=1
        )
        with self.assertRaises(ValueError):
            self.repo.addAssessment(assessment)

    def test_addAssessment_submitted_on_time_invalid_value(self):
        assessment = Assessment(
            assessment_id=None,
            student_id=1,
            assignment_name="Test",
            grade=85,
            submitted_on_time=2
        )
        with self.assertRaises(ValueError):
            self.repo.addAssessment(assessment)

    def test_addAssessment_submitted_on_time_negative(self):
        assessment = Assessment(
            assessment_id=None,
            student_id=1,
            assignment_name="Test",
            grade=85,
            submitted_on_time=-1
        )
        with self.assertRaises(ValueError):
            self.repo.addAssessment(assessment)

    # ========== String Field Edge Cases Tests ==========

    def test_addAssessment_empty_assignment_name(self):
        """Test assignment name as empty string"""
        assessment = Assessment(
            assessment_id=None,
            student_id=1,
            assignment_name="",
            grade=85,
            submitted_on_time=1
        )
        # Empty string should succeed (not None)
        assessment_id = self.repo.addAssessment(assessment)
        self.assertIsNotNone(assessment_id)

        added_assessment = self.repo.getAssessment(assessment_id)
        self.assertEqual(added_assessment.assignment_name, "")

    def test_addAssessment_very_long_assignment_name(self):
        """Test very long assignment name"""
        long_name = "A" * 1000
        assessment = Assessment(
            assessment_id=None,
            student_id=1,
            assignment_name=long_name,
            grade=85,
            submitted_on_time=1
        )
        assessment_id = self.repo.addAssessment(assessment)
        self.assertIsNotNone(assessment_id)

        added_assessment = self.repo.getAssessment(assessment_id)
        self.assertEqual(added_assessment.assignment_name, long_name)

    def test_addAssessment_assignment_name_with_special_chars(self):
        """Test assignment name with special characters"""
        assessment = Assessment(
            assessment_id=None,
            student_id=1,
            assignment_name="Test!@#$%^&*()",
            grade=85,
            submitted_on_time=1
        )
        assessment_id = self.repo.addAssessment(assessment)
        self.assertIsNotNone(assessment_id)

        added_assessment = self.repo.getAssessment(assessment_id)
        self.assertEqual(added_assessment.assignment_name, "Test!@#$%^&*()")

    def test_addAssessment_assignment_name_with_quotes(self):
        """Test assignment name with quotes"""
        assessment = Assessment(
            assessment_id=None,
            student_id=1,
            assignment_name="Test's \"Assignment\"",
            grade=85,
            submitted_on_time=1
        )
        assessment_id = self.repo.addAssessment(assessment)
        self.assertIsNotNone(assessment_id)

        added_assessment = self.repo.getAssessment(assessment_id)
        self.assertEqual(added_assessment.assignment_name, "Test's \"Assignment\"")

    def test_addAssessment_assignment_name_with_unicode(self):
        """Test assignment name with unicode characters"""
        assessment = Assessment(
            assessment_id=None,
            student_id=1,
            assignment_name="测试作业 🎓",
            grade=85,
            submitted_on_time=1
        )
        assessment_id = self.repo.addAssessment(assessment)
        self.assertIsNotNone(assessment_id)

        added_assessment = self.repo.getAssessment(assessment_id)
        self.assertEqual(added_assessment.assignment_name, "测试作业 🎓")

    def test_addAssessment_assignment_name_with_newlines(self):
        """Test assignment name with newline characters"""
        assessment = Assessment(
            assessment_id=None,
            student_id=1,
            assignment_name="Test\nAssignment",
            grade=85,
            submitted_on_time=1
        )
        assessment_id = self.repo.addAssessment(assessment)
        self.assertIsNotNone(assessment_id)

        added_assessment = self.repo.getAssessment(assessment_id)
        self.assertEqual(added_assessment.assignment_name, "Test\nAssignment")

    def test_addAssessment_assignment_name_with_tabs(self):
        """Test assignment name with tab characters"""
        assessment = Assessment(
            assessment_id=None,
            student_id=1,
            assignment_name="Test\tAssignment",
            grade=85,
            submitted_on_time=1
        )
        assessment_id = self.repo.addAssessment(assessment)
        self.assertIsNotNone(assessment_id)

        added_assessment = self.repo.getAssessment(assessment_id)
        self.assertEqual(added_assessment.assignment_name, "Test\tAssignment")

    def test_addAssessment_assignment_name_only_spaces(self):
        """Test assignment name with only spaces"""
        assessment = Assessment(
            assessment_id=None,
            student_id=1,
            assignment_name="   ",
            grade=85,
            submitted_on_time=1
        )
        assessment_id = self.repo.addAssessment(assessment)
        self.assertIsNotNone(assessment_id)

        added_assessment = self.repo.getAssessment(assessment_id)
        self.assertEqual(added_assessment.assignment_name, "   ")

    def test_addAssessment_assignment_name_sql_injection(self):
        """Test SQL injection attempt in assignment name"""
        assessment = Assessment(
            assessment_id=None,
            student_id=1,
            assignment_name="'; DROP TABLE assessments; --",
            grade=85,
            submitted_on_time=1
        )
        assessment_id = self.repo.addAssessment(assessment)
        self.assertIsNotNone(assessment_id)

        # Verify table still exists and data was stored safely
        added_assessment = self.repo.getAssessment(assessment_id)
        self.assertEqual(added_assessment.assignment_name, "'; DROP TABLE assessments; --")

    # ========== Data Type Edge Cases Tests ==========

    def test_addAssessment_grade_boundaries(self):
        """Test various grade values across the valid range"""
        test_grades = [1, 25, 50, 75, 99]

        for grade in test_grades:
            assessment = Assessment(
                assessment_id=None,
                student_id=1,
                assignment_name=f"Test Grade {grade}",
                grade=grade,
                submitted_on_time=1
            )
            assessment_id = self.repo.addAssessment(assessment)
            self.assertIsNotNone(assessment_id)

            added_assessment = self.repo.getAssessment(assessment_id)
            self.assertEqual(added_assessment.grade, grade)

    # ========== Duplicate and Multiple Records Tests ==========

    def test_addAssessment_duplicate_entry(self):
        """Test adding duplicate assessment for same student/assignment"""
        # Add first assessment
        assessment1 = Assessment(
            assessment_id=None,
            student_id=1,
            assignment_name="Duplicate Test",
            grade=85,
            submitted_on_time=1
        )
        assessment_id1 = self.repo.addAssessment(assessment1)

        # Add duplicate (same student, same assignment) - should succeed
        assessment2 = Assessment(
            assessment_id=None,
            student_id=1,
            assignment_name="Duplicate Test",
            grade=90,
            submitted_on_time=1
        )
        assessment_id2 = self.repo.addAssessment(assessment2)

        self.assertNotEqual(assessment_id1, assessment_id2)

    def test_addAssessment_multiple_same_student(self):
        """Test adding multiple assessments for same student"""
        assessment_ids = []
        for i in range(5):
            assessment = Assessment(
                assessment_id=None,
                student_id=2,
                assignment_name=f"Assignment {i}",
                grade=80 + i,
                submitted_on_time=1
            )
            assessment_id = self.repo.addAssessment(assessment)
            assessment_ids.append(assessment_id)

        self.assertEqual(len(assessment_ids), 5)
        self.assertEqual(len(set(assessment_ids)), 5)  # All unique IDs

    def test_addAssessment_same_assignment_multiple_students(self):
        """Test same assignment for different students"""
        assessment_ids = []
        for student_id in [1, 2, 3]:
            assessment = Assessment(
                assessment_id=None,
                student_id=student_id,
                assignment_name="Common Assignment",
                grade=85,
                submitted_on_time=1
            )
            assessment_id = self.repo.addAssessment(assessment)
            assessment_ids.append(assessment_id)

        self.assertEqual(len(assessment_ids), 3)
        self.assertEqual(len(set(assessment_ids)), 3)  # All unique IDs

    # ========== Query Tests ==========

    def test_getAssessmentsByStudentID_single(self):
        """Test getting assessments for student with one assessment"""
        assessment = Assessment(
            assessment_id=None,
            student_id=1,
            assignment_name="Single Assessment",
            grade=85,
            submitted_on_time=1
        )
        self.repo.addAssessment(assessment)

        assessments = self.repo.getAssessmentsByStudentID(1)
        self.assertIsNotNone(assessments)
        self.assertGreater(len(assessments), 0)

    def test_getAssessmentsByStudentID_multiple(self):
        """Test getting assessments for student with multiple assessments"""
        for i in range(3):
            assessment = Assessment(
                assessment_id=None,
                student_id=2,
                assignment_name=f"Multiple Assessment {i}",
                grade=80 + i,
                submitted_on_time=1
            )
            self.repo.addAssessment(assessment)

        assessments = self.repo.getAssessmentsByStudentID(2)
        self.assertIsNotNone(assessments)
        self.assertGreaterEqual(len(assessments), 3)

    def test_getAssessmentsByStudentID_nonexistent(self):
        """Test getting assessments for non-existent student"""
        assessments = self.repo.getAssessmentsByStudentID(99999)
        self.assertIsNone(assessments)

    def test_getAssessment_negative_id(self):
        """Test getting assessment with negative ID"""
        assessment = self.repo.getAssessment(-1)
        self.assertIsNone(assessment)

    def test_getAssessments_verify_count(self):
        """Test that getAssessments returns expected number of records"""
        initial_assessments = self.repo.getAssessments()
        initial_count = len(initial_assessments) if initial_assessments else 0

        # Add 3 new assessments
        for i in range(3):
            assessment = Assessment(
                assessment_id=None,
                student_id=1,
                assignment_name=f"Count Test {i}",
                grade=85,
                submitted_on_time=1
            )
            self.repo.addAssessment(assessment)

        final_assessments = self.repo.getAssessments()
        final_count = len(final_assessments) if final_assessments else 0
        self.assertEqual(final_count, initial_count + 3)

    # ========== Delete Tests ==========

    def test_deleteAssessmentsByStudentID_single(self):
        """Test deleting single assessment"""
        assessment = Assessment(
            assessment_id=None,
            student_id=1,
            assignment_name="Delete Single",
            grade=85,
            submitted_on_time=1
        )
        assessment_id = self.repo.addAssessment(assessment)

        # Verify it exists
        self.assertIsNotNone(self.repo.getAssessment(assessment_id))

        # Delete
        self.repo.deleteAssessmentsByStudentID(1)

    def test_deleteAssessmentsByStudentID_multiple(self):
        """Test deleting multiple assessments"""
        assessment_ids = []
        for i in range(3):
            assessment = Assessment(
                assessment_id=None,
                student_id=3,
                assignment_name=f"Delete Multiple {i}",
                grade=85,
                submitted_on_time=1
            )
            assessment_id = self.repo.addAssessment(assessment)
            assessment_ids.append(assessment_id)

        # Delete all assessments for student 3
        self.repo.deleteAssessmentsByStudentID(3)

        # Verify all are deleted
        for assessment_id in assessment_ids:
            self.assertIsNone(self.repo.getAssessment(assessment_id))

    def test_deleteAssessmentsByStudentID_nonexistent(self):
        """Test deleting assessments for non-existent student doesn't crash"""
        try:
            self.repo.deleteAssessmentsByStudentID(99999)
        except Exception as e:
            self.fail(f"Delete for nonexistent student raised exception: {e}")

    def test_deleteAssessmentsByStudentID_verify_cascade(self):
        """Test that delete only affects target student's assessments"""
        # Add assessments for two different students
        assessment1 = Assessment(
            assessment_id=None,
            student_id=1,
            assignment_name="Student 1 Assessment",
            grade=85,
            submitted_on_time=1
        )
        assessment_id1 = self.repo.addAssessment(assessment1)

        assessment2 = Assessment(
            assessment_id=None,
            student_id=2,
            assignment_name="Student 2 Assessment",
            grade=90,
            submitted_on_time=1
        )
        assessment_id2 = self.repo.addAssessment(assessment2)

        # Delete assessments for student 1
        self.repo.deleteAssessmentsByStudentID(1)

        # Verify student 2's assessment still exists
        remaining_assessment = self.repo.getAssessment(assessment_id2)
        self.assertIsNotNone(remaining_assessment)
        self.assertEqual(remaining_assessment.student_id, 2)

    # ========== Edge Cases Tests ==========

    def test_addAssessment_specified_id(self):
        """Test manually specifying assessment_id"""
        assessment = Assessment(
            assessment_id=50000,
            student_id=1,
            assignment_name="Specified ID Test",
            grade=85,
            submitted_on_time=1
        )
        assessment_id = self.repo.addAssessment(assessment)
        self.assertEqual(assessment_id, 50000)

        # Verify it was added with that ID
        added_assessment = self.repo.getAssessment(50000)
        self.assertIsNotNone(added_assessment)
        self.assertEqual(added_assessment.assessment_id, 50000)

    def test_addAssessment_grade_distribution(self):
        """Test full grade distribution from 0 to 100"""
        # Test every 10th grade
        for grade in range(0, 101, 10):
            assessment = Assessment(
                assessment_id=None,
                student_id=1,
                assignment_name=f"Grade {grade} Test",
                grade=grade,
                submitted_on_time=1
            )
            assessment_id = self.repo.addAssessment(assessment)
            self.assertIsNotNone(assessment_id)

            added_assessment = self.repo.getAssessment(assessment_id)
            self.assertEqual(added_assessment.grade, grade)

    def test_addAssessment_assignment_name_trimming(self):
        """Test if whitespace is preserved in assignment names"""
        names_with_spaces = [
            "  Leading spaces",
            "Trailing spaces  ",
            "  Both sides  ",
            "Mid  dle  spaces"
        ]

        for name in names_with_spaces:
            assessment = Assessment(
                assessment_id=None,
                student_id=1,
                assignment_name=name,
                grade=85,
                submitted_on_time=1
            )
            assessment_id = self.repo.addAssessment(assessment)
            self.assertIsNotNone(assessment_id)

            added_assessment = self.repo.getAssessment(assessment_id)
            # Whitespace should be preserved exactly
            self.assertEqual(added_assessment.assignment_name, name)

if __name__ == "__main__":
    unittest.main()
