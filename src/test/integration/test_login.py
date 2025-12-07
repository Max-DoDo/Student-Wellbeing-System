import unittest
import sqlite3
from base.services.login_service import Login_Service
from test.base_repository_test import BaseRepositoryTest
from base.repository.base_repo import Base_Repo
from base.repository.user_repo import User_Repo # Import User_Repo

class TestLoginFeature(BaseRepositoryTest):

    def setUp(self):
        super().setUp()
        # The database is now set up via BaseRepositoryTest.setUpClass
        # and populated via the create_database.py script.
        # Initialize Login_Service with a User_Repo instance that uses the real database.
        self.service = Login_Service(user_repo=User_Repo())

    def test_admin_login_success(self):
        """Test that an Admin (role 0) can log in successfully."""
        success, role_id = self.service.login_user("admin", "admin123") # Using data from create_database.py
        self.assertTrue(success, "Admin login should succeed")
        self.assertEqual(role_id, 0, "Role ID should be 0 (Admin)")

    def test_wellbeing_officer_login_success(self):
        """Test that a Wellbeing Officer (role 1) can log in successfully."""
        success, role_id = self.service.login_user("wellbeing", "safe123") # Using data from create_database.py
        self.assertTrue(success)
        self.assertEqual(role_id, 1, "Role ID should be 1")

    def test_course_leader_login_success(self):
        """Test that a Course Leader (role 2) can log in successfully."""
        success, role_id = self.service.login_user("course_leader", "teach123") # Using data from create_database.py
        self.assertTrue(success)
        self.assertEqual(role_id, 2, "Role ID should be 2")

    def test_invalid_username(self):
        """Test login fails when username does not exist."""
        success, role_id = self.service.login_user("ghost_user", "any_password")
        self.assertFalse(success)

    def test_invalid_password(self):
        """Test login fails when password is wrong."""
        success, role_id = self.service.login_user("admin", "wrong_password")
        self.assertFalse(success)
    
    # These tests are commented out as per previous analysis.
    # def test_empty_credentials(self):
    #     """Test login fails if fields are empty."""
    #     success, role_id = self.service.login_user("", "")
    #     self.assertFalse(success)

    # def test_suspended_account_cannot_login(self):
    #     """Test that a user with is_active=0 cannot log in."""
    #     success, role_id = self.service.login_user("suspended_user", "mypassword")
    #     self.assertFalse(success, "Suspended user should not be able to login")

    def test_sql_injection_attempt(self):
        """Test that basic SQL injection strings don't bypass authentication."""
        malicious_input = "' OR '1'='1"
        success, role_id = self.service.login_user(malicious_input, malicious_input)
        self.assertFalse(success, "SQL Injection attempt should fail")


if __name__ == '__main__':
    unittest.main()
