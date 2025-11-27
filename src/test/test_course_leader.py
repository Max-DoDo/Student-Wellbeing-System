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


if __name__ == '__main__':
    unittest.main()