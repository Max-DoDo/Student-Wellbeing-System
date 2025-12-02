import unittest
import sys
import os
import sqlite3

CURRENT_DIR = os.path.dirname(__file__)
SRC_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", ".." ,".."))
sys.path.insert(0, SRC_PATH)

from test.base_test.repository_test.base_repo_test import Base_Repo_test

TEST_DB = "test_base_repo.db"


class TestBaseRepo(unittest.TestCase):
    
    def setUp(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

        conn = sqlite3.connect(TEST_DB)
        conn.close()

        Base_Repo_test.set_db_path_test(TEST_DB)
        self.repo = Base_Repo_test()

    def tearDown(self):
        self.repo.close()
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_initialization_creates_connection(self):
        """Initialization sets up connection and cursor."""
        self.assertIsNotNone(self.repo.conn)
        self.assertIsNotNone(self.repo.cursor)

    def test_cursor_is_sqlite_cursor(self):
        """Cursor should be sqlite3.Cursor."""
        self.assertIsInstance(self.repo.cursor, sqlite3.Cursor)

    def test_set_db_path_test(self):
        """Setting DB_PATH_test updates class variable."""
        Base_Repo_test.set_db_path_test("new_test.db")
        self.assertEqual(Base_Repo_test.DB_PATH_test, "new_test.db")

    def test_close(self):
        """close() should close the connection."""
        self.repo.close()
        with self.assertRaises(sqlite3.ProgrammingError):
            self.repo.cursor.execute("SELECT 1")


if __name__ == "__main__":
    unittest.main()
