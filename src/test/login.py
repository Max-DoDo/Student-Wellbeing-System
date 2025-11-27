import unittest
import sqlite3
import sys
import os

# -----------------------------------------------------------------------
# 1. Setup the path so Python can find 'src'
# -----------------------------------------------------------------------
# Get the absolute path of the current file (src/test/login.py)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go up two levels to find the project root (the folder containing 'src')
project_root = os.path.abspath(os.path.join(current_dir, '../../'))

# Add the project root to sys.path
sys.path.insert(0, project_root)

from src.base.services.Login import login_user

TEST_DB_NAME = "test_university_wellbeing.db"

class TestLoginFeature(unittest.TestCase):

    def setUp(self):
        """
        Runs BEFORE every single test.
        Sets up a fresh database with the schema and some dummy data.
        """
        self.conn = sqlite3.connect(TEST_DB_NAME)
        self.cursor = self.conn.cursor()
        
        # 1. Initialize Schema (Copied from your script, shortened for brevity)
        self.cursor.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                users_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                role_id INTEGER NOT NULL,
                is_active INTEGER DEFAULT 1 CHECK(is_active IN (0, 1)),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # 2. Seed Data (Insert test users)
        users = [
            # (username, password, first, last, email, role, is_active)
            ("admin_user", "adminpass", "Admin", "User", "admin@uni.edu", 0, 1),
            ("wellbeing_officer", "officerpass", "Well", "Being", "officer@uni.edu", 1, 1),
            ("course_leader", "leaderpass", "Course", "Leader", "leader@uni.edu", 2, 1),
            ("suspended_user", "mypassword", "Bad", "User", "bad@uni.edu", 1, 0), # Suspended!
        ]
        self.cursor.executemany("""
            INSERT INTO users (username, password, first_name, last_name, email, role_id, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, users)
        self.conn.commit()

    def tearDown(self):
        """
        Runs AFTER every single test.
        Closes the connection and deletes the test database file.
        """
        self.conn.close()
        if os.path.exists(TEST_DB_NAME):
            os.remove(TEST_DB_NAME)

    # ==========================================
    # Success Scenarios
    # ==========================================

    def test_admin_login_success(self):
        """Test that an Admin (role 0) can log in successfully."""
        result = login_user(TEST_DB_NAME, "admin_user", "adminpass")
        
        self.assertTrue(result['success'], "Admin login should succeed")
        self.assertEqual(result['role_id'], 0, "Role ID should be 0 (Admin)")
        self.assertEqual(result['message'], "Login successful")

    def test_wellbeing_officer_login_success(self):
        """Test that a Wellbeing Officer (role 1) can log in successfully."""
        result = login_user(TEST_DB_NAME, "wellbeing_officer", "officerpass")
        
        self.assertTrue(result['success'])
        self.assertEqual(result['role_id'], 1, "Role ID should be 1")

    def test_course_leader_login_success(self):
        """Test that a Course Leader (role 2) can log in successfully."""
        result = login_user(TEST_DB_NAME, "course_leader", "leaderpass")
        
        self.assertTrue(result['success'])
        self.assertEqual(result['role_id'], 2, "Role ID should be 2")

    # ==========================================
    # Failure Scenarios
    # ==========================================

    def test_invalid_username(self):
        """Test login fails when username does not exist."""
        result = login_user(TEST_DB_NAME, "ghost_user", "any_password")
        
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], "Invalid username or password")

    def test_invalid_password(self):
        """Test login fails when password is wrong."""
        result = login_user(TEST_DB_NAME, "admin_user", "wrong_password")
        
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], "Invalid username or password")

    def test_empty_credentials(self):
        """Test login fails if fields are empty."""
        result = login_user(TEST_DB_NAME, "", "")
        
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], "Username and password are required")

    # ==========================================
    # BUSINESS LOGIC & EDGE CASES
    # ==========================================

    def test_suspended_account_cannot_login(self):
        """Test that a user with is_active=0 cannot log in."""
        result = login_user(TEST_DB_NAME, "suspended_user", "mypassword")
        
        self.assertFalse(result['success'], "Suspended user should not be able to login")
        self.assertEqual(result['message'], "Account is suspended. Please contact admin.")

    def test_sql_injection_attempt(self):
        """Test that basic SQL injection strings don't bypass authentication."""
        # This input tries to trick the SQL query into always returning True
        malicious_input = "' OR '1'='1"
        result = login_user(TEST_DB_NAME, malicious_input, malicious_input)
        
        self.assertFalse(result['success'], "SQL Injection attempt should fail")
        self.assertNotEqual(result['role_id'], 0, "Should not gain admin access via injection")

if __name__ == '__main__':
    unittest.main()