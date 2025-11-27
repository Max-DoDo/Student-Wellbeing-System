import unittest
import sqlite3
import os

def add_attendance(db_name, student_id, week, is_present):
    """Placeholder: Always fails or does nothing"""
    print(f"[STUB] add_attendance called for student {student_id}")
    return False

def get_attendance_by_week(db_name, week):
    """Placeholder: Returns empty list"""
    return []

def add_assessment(db_name, student_id, name, grade):
    """Placeholder: Always fails"""
    return False

def calculate_student_average(db_name, student_id):
    """Placeholder: Returns 0"""
    return 0.0

def get_course_average_grade(db_name):
    """Placeholder: Returns 0"""
    return 0.0

# ===========================================================================
# END PLACEHOLDERS
# ===========================================================================

TEST_DB_NAME = "test_course_leader.db"

class TestCourseLeaderFeatures(unittest.TestCase):

    def setUp(self):
        self.conn = sqlite3.connect(TEST_DB_NAME)
        self.cursor = self.conn.cursor()
        
        # Schema setup (Course Leader focuses on Attendance & Grades)
        self.cursor.executescript("""
            CREATE TABLE students (student_id INTEGER PRIMARY KEY, first_name TEXT);
            
            CREATE TABLE attendance (
                attendance_id INTEGER PRIMARY KEY, student_id INTEGER, 
                week_number INTEGER CHECK(week_number BETWEEN 1 AND 52), 
                is_present INTEGER
            );
            
            CREATE TABLE assessments (
                assessment_id INTEGER PRIMARY KEY, student_id INTEGER, 
                assignment_name TEXT, grade INTEGER CHECK(grade BETWEEN 0 AND 100)
            );
        """)
        # Seed Data
        self.cursor.execute("INSERT INTO students (student_id, first_name) VALUES (1, 'Alice')")
        self.cursor.execute("INSERT INTO students (student_id, first_name) VALUES (2, 'Bob')")
        self.conn.commit()

    def tearDown(self):
        self.conn.close()
        if os.path.exists(TEST_DB_NAME):
            os.remove(TEST_DB_NAME)

    def test_insert_attendance_valid(self):
        """TC-009: Verify Course Leader can record attendance."""
        success = add_attendance(TEST_DB_NAME, student_id=1, week=5, is_present=1)
        self.assertTrue(success)
        
        # Verify in DB
        self.cursor.execute("SELECT is_present FROM attendance WHERE student_id=1 AND week_number=5")
        result = self.cursor.fetchone()
        if result:
            self.assertEqual(result[0], 1)

    def test_insert_attendance_invalid_week(self):
        """Edge Case: Ensure Course Leader cannot input invalid weeks."""
        with self.assertRaises(sqlite3.IntegrityError):
            add_attendance(TEST_DB_NAME, student_id=1, week=53, is_present=1)

    def test_retrieve_weekly_attendance(self):
        """TC-010: Verify Course Leader can view class attendance list."""
        add_attendance(TEST_DB_NAME, student_id=1, week=2, is_present=1) 
        add_attendance(TEST_DB_NAME, student_id=2, week=2, is_present=0) 

        report = get_attendance_by_week(TEST_DB_NAME, week=2)
        
        self.assertEqual(len(report), 2)
        # Check specific values
        alice = next((r for r in report if r['student_id'] == 1), None)
        if alice:
            self.assertEqual(alice['is_present'], 1)

    # ==========================================
    # GRADE MANAGEMENT (FR-007, FR-012)
    # ==========================================

    def test_insert_grade_valid(self):
        """Verify Course Leader can input grades."""
        success = add_assessment(TEST_DB_NAME, student_id=1, name="Math 101", grade=85)
        self.assertTrue(success)

    def test_insert_grade_invalid_range(self):
        """Edge Case: Grades must be 0-100."""
        with self.assertRaises(sqlite3.IntegrityError):
            add_assessment(TEST_DB_NAME, 1, "Math 101", 105)

    def test_calculate_student_average(self):
        """Verify individual student average calculation."""
        add_assessment(TEST_DB_NAME, 1, "Test 1", 80)
        add_assessment(TEST_DB_NAME, 1, "Test 2", 90)
        add_assessment(TEST_DB_NAME, 1, "Test 3", 100)

        avg = calculate_student_average(TEST_DB_NAME, student_id=1)
        self.assertEqual(avg, 90.0)

    def test_calculate_average_no_grades(self):
        """Edge Case: Student with no grades should return 0, not crash."""
        avg = calculate_student_average(TEST_DB_NAME, student_id=2) 
        self.assertEqual(avg, 0) 

    def test_group_performance_metrics(self):
        """Verify Course Leader can view overall class performance."""
        add_assessment(TEST_DB_NAME, 1, "T1", 90)
        add_assessment(TEST_DB_NAME, 2, "T1", 70)

        class_avg = get_course_average_grade(TEST_DB_NAME)
        self.assertEqual(class_avg, 80.0)

if __name__ == '__main__':
    unittest.main()