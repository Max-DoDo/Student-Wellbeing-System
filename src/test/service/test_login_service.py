import unittest
from unittest.mock import MagicMock
from base.services.login_service import Login_Service
from base.entity.user import User # Use the real User entity

class TestLoginService(unittest.TestCase):

    def setUp(self):
        self.user_repo = MagicMock()
        self.service = Login_Service(user_repo=self.user_repo) # Inject the mocked user_repo

    def test_login_correct_credentials(self):
        """Login should succeed with correct username & password."""
        user = User(id=1, username="alice123", password="pw1", role_id=2, first_name="Alice", last_name="Brown", email="a@a.com", is_active=True, created_at="2024-12-11")
        self.user_repo.getUserByUserName.return_value = user
        
        result = self.service.login_user("alice123", "pw1")
        
        self.assertEqual(result, [True, 2])
        self.user_repo.getUserByUserName.assert_called_once_with("alice123") # This should now work

    def test_login_wrong_password(self):
        """Login should fail when password is incorrect."""
        user = User(id=1, username="alice123", password="pw1", role_id=2, first_name="Alice", last_name="Brown", email="a@a.com", is_active=True, created_at="2024-12-11")
        self.user_repo.getUserByUserName.return_value = user
        
        result = self.service.login_user("alice123", "wrongpw")
        
        self.assertEqual(result, [False, -1])
        self.user_repo.getUserByUserName.assert_called_once_with("alice123") # This should now work

    def test_login_username_not_found(self):
        """Login should fail when username does not exist."""
        self.user_repo.getUserByUserName.return_value = None
        
        result = self.service.login_user("unknown", "pw1")
        
        self.assertEqual(result, [False, -1])
        self.user_repo.getUserByUserName.assert_called_once_with("unknown") # This should now work

    def test_login_inactive_user(self):
        """
        Login works even if user is inactive.
        (Service does NOT check is_active)
        """
        user = User(id=1, username="boblee", password="pw2", role_id=3, is_active=False, first_name="Bob", last_name="Lee", email="b@b.com", created_at="2024-12-11")
        self.user_repo.getUserByUserName.return_value = user
        
        result = self.service.login_user("boblee", "pw2")
        
        self.assertEqual(result, [True, 3])
        self.user_repo.getUserByUserName.assert_called_once_with("boblee") # This should now work


if __name__ == "__main__":
    unittest.main()
