import unittest
import sys
import os

CURRENT_DIR = os.path.dirname(__file__)
SRC_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", "..", ".."))
sys.path.insert(0, SRC_PATH)

import sqlite3

from test.base_test.repository_test.base_repo_test import Base_Repo_test
from test.base_test.services_test.login_service_test import Login_Service_test
from test.base_test.repository_test.user_repo_test import User_Repo_test


TEST_DB = "test_login_service.db"


class TestLoginService(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

        Base_Repo_test.set_db_path_test(TEST_DB)

        self.user_repo = User_Repo_test()
        self.user_repo.conn.row_factory = sqlite3.Row
        self.user_repo.cursor = self.user_repo.conn.cursor()

        self.service = Login_Service_test()

        self.user_repo.cursor.executescript("""
            CREATE TABLE users (
                users_id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                email TEXT,
                username TEXT,
                password TEXT,
                role_id INTEGER,
                is_active INTEGER,
                created_at TEXT
            );
        """)

        self.user_repo.cursor.execute("""
            INSERT INTO users
            (users_id, first_name, last_name, email, username, password, role_id, is_active, created_at)
            VALUES (1, 'Alice', 'Brown', 'alice@mail.com', 'alice123', 'pw1', 2, 1, '2024-12-10')
        """)

        self.user_repo.cursor.execute("""
            INSERT INTO users
            (users_id, first_name, last_name, email, username, password, role_id, is_active, created_at)
            VALUES (2, 'Bob', 'Lee', 'bob@mail.com', 'boblee', 'pw2', 3, 0, '2024-12-11')
        """)

        self.user_repo.conn.commit()

    def tearDown(self):
        try:
            self.user_repo.conn.close()
        except:
            pass

        if os.path.exists(TEST_DB):
            try:
                os.remove(TEST_DB)
            except:
                pass

    # ==========================================================
    # TEST CASES
    # ==========================================================

    def test_login_correct_credentials(self):
        """Login should succeed with correct username & password."""
        result = self.service.login_user("alice123", "pw1")
        self.assertEqual(result, [True, 2])  # True + role_id = 2

    def test_login_wrong_password(self):
        """Login should fail when password is incorrect."""
        result = self.service.login_user("alice123", "wrongpw")
        self.assertEqual(result, [False, -1])

    def test_login_username_not_found(self):
        """Login should fail when username does not exist."""
        result = self.service.login_user("unknown", "pw1")
        self.assertEqual(result, [False, -1])

    def test_login_inactive_user(self):
        """
        Login works even if user is inactive.
        (Service does NOT check is_active)
        """
        result = self.service.login_user("boblee", "pw2")
        self.assertEqual(result, [True, 3])   # role_id = 3


if __name__ == "__main__":
    unittest.main()
