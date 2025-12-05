import unittest
from base.repository.user_repo import User_Repo
from base.entity.user import User
from test_refactored.base_repository_test import BaseRepositoryTest

class TestUserRepo(BaseRepositoryTest):

    def setUp(self):
        self.repo = User_Repo()

    def test_getUser(self):
        """Test fetching a user by ID."""
        u = self.repo.getUser(1)
        self.assertIsNotNone(u)
        # self.assertEqual(u.id, 1)

    def test_getUser_not_found(self):
        """Test fetching a non-existing user returns None."""
        u = self.repo.getUser(9999)
        self.assertIsNone(u)

    def test_getUserByUserName(self):
        """Test fetching a user by username."""
        u = self.repo.getUserByUserName("admin") # Assuming 'admin' is a user in the database
        self.assertIsNotNone(u)
        # self.assertEqual(u.username, "admin")

    def test_getUserByUserName_not_found(self):
        """Test fetching a username not in table returns None."""
        u = self.repo.getUserByUserName("unknown_user")
        self.assertIsNone(u)

    def test_getAllUser(self):
        """Test fetching all users returns correct list."""
        users = self.repo.getAllUser()
        self.assertIsInstance(users, list)
        self.assertGreater(len(users), 0) # Assuming there's at least one user

if __name__ == "__main__":
    unittest.main()
