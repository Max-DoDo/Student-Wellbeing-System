import unittest
import sys
import os

CURRENT_DIR = os.path.dirname(__file__)

SRC_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", ".." ,".." ))
sys.path.insert(0, SRC_PATH)
import sqlite3

# ===========================================================================
# PLACEHOLDERS (STUBS)
# ===========================================================================

from test.base_test.repository_test.user_repo_test import User_Repo_test
from test.base_test.entity_test.user_test import User_test
from test.base_test.repository_test.base_repo_test import Base_Repo_test

TEST_DB = "test_user_repo.db"
print(">>> THIS IS THE REAL TEST USER REPO FILE <<<")
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

        Base_Repo_test.set_db_path_test(TEST_DB)
        self.repo = User_Repo_test()
        self.repo.conn.row_factory = sqlite3.Row
        self.repo.cursor = self.repo.conn.cursor()

        self.cursor = self.repo.cursor

        self.cursor.executescript("""
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

        self.cursor.execute("""
            INSERT INTO users
            (users_id, first_name, last_name, email, username, password, role_id, is_active, created_at)
            VALUES (1, 'Alice', 'Brown', 'a@a.com', 'alice123', '123', 2, 1, '2024-12-11')
        """)

        self.repo.conn.commit()


    def tearDown(self):
        try:
            self.repo.conn.close()
        except:
            pass

        del self.repo

        if os.path.exists(TEST_DB):
            try:
                os.remove(TEST_DB)
            except:
                pass

    def test_getUser_test(self):
        """Test fetching a user by ID."""
        u = self.repo.getUser(1)

        self.assertIsNotNone(u)
        self.assertEqual(u.id, 1)
        self.assertEqual(u.first_name, "Alice")
        self.assertEqual(u.username, "alice123")

    def test_getUser_test_not_found(self):
        """Test fetching a non-existing user returns None."""
        u = self.repo.getUser(999)
        self.assertIsNone(u)

    def test_getUserByUserName_test(self):
        """Test fetching a user by username."""
        u = self.repo.getUserByUserName("alice123")

        self.assertIsNotNone(u)
        self.assertEqual(u.username, "alice123")
        self.assertEqual(u.email, "a@a.com")

    def test_getUserByUserName_test_not_found(self):
        """Test fetching a username not in table returns None."""
        u = self.repo.getUserByUserName("unknown_user")
        self.assertIsNone(u)

    def test_getAllUser_test(self):
        """Test fetching all users returns correct list."""
        users = self.repo.getAllUser()

        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].id, 1)

    def test_toUser_test(self):
        """Test converting a DB row to User object."""
        self.cursor.execute("SELECT * FROM users WHERE users_id = 1")
        row = self.cursor.fetchone()

        obj = self.repo.toUser(row)

        self.assertIsInstance(obj, User_test)
        self.assertEqual(obj.id, 1)
        self.assertEqual(obj.username, "alice123")

    def test_toUsers_test(self):
        """Test converting multiple user rows to User list."""
        self.cursor.execute("SELECT * FROM users")
        rows = self.cursor.fetchall()

        users = self.repo.toUsers(rows)

        self.assertEqual(len(users), 1)
        self.assertIsInstance(users[0], User_test)



if __name__ == "__main__":
    unittest.main()
