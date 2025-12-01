import unittest
import sys
import os

CURRENT_DIR = os.path.dirname(__file__)

SRC_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..",".."))
sys.path.insert(0, SRC_PATH)
import sqlite3

# ===========================================================================
# PLACEHOLDERS (STUBS)
# ===========================================================================

from repository_test.user_repo_test import User_Repo_test
from entity_test.user_test import User_test
from repository_test.base_repo_test import Base_Repo_test

TEST_DB = "test_user_repo.db"

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


class TestUserRepo(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

        self.conn, self.cursor = setup_test_db()
        Base_Repo_test.set_db_path_test(TEST_DB)
        self.repo = User_Repo_test()

        # Insert initial test user
        self.cursor.execute("""
            INSERT INTO users
            (users_id, first_name, last_name, email, username, password, role_id, is_active, created_at)
            VALUES (1, 'Alice', 'Smith', 'alice@mail.com', 'alice123', 'pw1', 2, 1, '2025-01-01')
        """)
        self.conn.commit()

    def tearDown(self):
        self.conn.close()
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_getUser_test(self):
        """Test fetching a user by ID."""
        u = self.repo.getUser_test(1)

        self.assertIsNotNone(u)
        self.assertEqual(u.id_test, 1)
        self.assertEqual(u.first_name_test, "Alice")
        self.assertEqual(u.username_test, "alice123")

    def test_getUser_test_not_found(self):
        """Test fetching a non-existing user returns None."""
        u = self.repo.getUser_test(999)
        self.assertIsNone(u)

    def test_getUserByUserName_test(self):
        """Test fetching a user by username."""
        u = self.repo.getUserByUserName_test("alice123")

        self.assertIsNotNone(u)
        self.assertEqual(u.username_test, "alice123")
        self.assertEqual(u.email_test, "alice@mail.com")

    def test_getUserByUserName_test_not_found(self):
        """Test fetching a username not in table returns None."""
        u = self.repo.getUserByUserName_test("unknown_user")
        self.assertIsNone(u)

    def test_getAllUser_test(self):
        """Test fetching all users returns correct list."""
        users = self.repo.getAllUser_test()

        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].id_test, 1)

    def test_toUser_test(self):
        """Test converting a DB row to User_test object."""
        self.cursor.execute("SELECT * FROM users WHERE users_id = 1")
        row = self.cursor.fetchone()

        obj = self.repo.toUser_test(row)

        self.assertIsInstance(obj, User_test)
        self.assertEqual(obj.id_test, 1)
        self.assertEqual(obj.username_test, "alice123")

    def test_toUsers_test(self):
        """Test converting multiple user rows to User_test list."""
        self.cursor.execute("SELECT * FROM users")
        rows = self.cursor.fetchall()

        users = self.repo.toUsers_test(rows)

        self.assertEqual(len(users), 1)
        self.assertIsInstance(users[0], User_test)


if __name__ == "__main__":
    unittest.main()
