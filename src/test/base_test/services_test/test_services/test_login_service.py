import unittest
import sys
import os

CURRENT_DIR = os.path.dirname(__file__)

SRC_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".." ))
sys.path.insert(0, SRC_PATH)

import sqlite3

# ===========================================================================
# PLACEHOLDERS (STUBS)
# ===========================================================================

from repository_test.base_repo_test import Base_Repo_test
from repository_test.user_repo_test import User_Repo_test
from entity_test.user_test import User_test
from services_test.login_service_test import Login_Service_test

TEST_DB = "test_login_service.db"

def setup_test_db():
    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()
    cursor.executescript("""
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
    conn.commit()
    return conn, cursor

# ===========================================================================
# END PLACEHOLDERS
# ===========================================================================


class TestLoginService(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

        self.conn, self.cursor = setup_test_db()
        Base_Repo_test.set_db_path_test(TEST_DB)

        # Insert a valid user for testing login
        self.cursor.execute("""
            INSERT INTO users
            (users_id, first_name, last_name, email, username, password, role_id, is_active, created_at)
            VALUES (1, 'Alice', 'Smith', 'alice@mail.com', 'alice123', 'pw1', 2, 1, '2025-01-01')
        """)
        self.conn.commit()

        self.service = Login_Service_test()

    def tearDown(self):
        self.conn.close()
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_login_correct_credentials(self):
        """Test login returns True when username and password match."""
        result = self.service.login_user_test("alice123", "pw1")

        self.assertEqual(result[0], True)   # success flag
        self.assertEqual(result[1], 2)      # role_id_test

    def test_login_wrong_password(self):
        """Test login returns False when password is incorrect."""
        result = self.service.login_user_test("alice123", "wrongpw")

        self.assertEqual(result[0], False)
        self.assertEqual(result[1], -1)

    def test_login_username_not_found(self):
        """Test login returns False when username does not exist."""
        result = self.service.login_user_test("unknown_user", "pw1")

        self.assertEqual(result[0], False)
        self.assertEqual(result[1], -1)

    def test_login_inactive_user(self):
        """Test login still works even if user is inactive (repo does not check is_active)."""
        self.cursor.execute("""
            INSERT INTO users
            (users_id, first_name, last_name, email, username, password, role_id, is_active, created_at)
            VALUES (2, 'Bob', 'Lee', 'bob@mail.com', 'boblee', 'pw2', 3, 0, '2025-01-02')
        """)
        self.conn.commit()

        result = self.service.login_user_test("boblee", "pw2")

        self.assertEqual(result[0], True)
        self.assertEqual(result[1], 3)

if __name__ == "__main__":
    unittest.main()
