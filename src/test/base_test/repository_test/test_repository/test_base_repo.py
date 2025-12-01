import unittest
import sys
import os

CURRENT_DIR = os.path.dirname(__file__)

SRC_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
sys.path.insert(0, SRC_PATH)
import sqlite3

# ===========================================================================
# PLACEHOLDERS (STUBS)
# ===========================================================================

from repository_test.base_repo_test import Base_Repo_test

TEST_DB = "test_base_repo.db"

# ===========================================================================
# END PLACEHOLDERS
# ===========================================================================


class TestBaseRepoTest(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

        # Create empty sqlite DB for testing
        conn = sqlite3.connect(TEST_DB)
        conn.close()

        Base_Repo_test.set_db_path_test(TEST_DB)
        self.repo = Base_Repo_test()

    def tearDown(self):
        self.repo.close_test()
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_initialization_creates_connection(self):
        """Test that initialization creates a database connection."""
        self.assertIsNotNone(self.repo.conn_test)
        self.assertIsNotNone(self.repo.cursor_test)

    def test_cursor_is_sqlite_cursor(self):
        """Test that cursor_test is an sqlite3.Cursor instance."""
        self.assertIsInstance(self.repo.cursor_test, sqlite3.Cursor)

    def test_set_db_path_test(self):
        """Test setting the DB_PATH_test class variable."""
        Base_Repo_test.set_db_path_test("new_test.db")
        self.assertEqual(Base_Repo_test.DB_PATH_test, "new_test.db")

    def test_close_test(self):
        """Test that close_test closes the connection."""
        self.repo.close_test()
        # Connection should be closed; trying to use it should cause an error
        with self.assertRaises(sqlite3.ProgrammingError):
            self.repo.cursor_test.execute("SELECT 1")


if __name__ == "__main__":
    unittest.main()
