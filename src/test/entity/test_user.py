import unittest
from base.entity.user import User

class TestUserEntity(unittest.TestCase):

    def test_initialization_fields(self):
        """Test that provided fields are assigned correctly."""
        u = User(
            id=1,
            first_name="Alice",
            last_name="Smith",
            name=None,
            gender="F",
            email="alice@example.com",
            username="alice123",
            password="pw1",
            role_id=2,
            is_active=True,
            created_at="2025-01-01"
        )
        self.assertEqual(u.id, 1)
        self.assertEqual(u.first_name, "Alice")
        self.assertEqual(u.last_name, "Smith")
        self.assertEqual(u.username, "alice123")
        self.assertEqual(u.password, "pw1")
        self.assertEqual(u.role_id, 2)
        self.assertTrue(u.is_active)
        self.assertEqual(u.created_at, "2025-01-01")

    def test_inherited_person_fields(self):
        """Test that User inherits fields defined in Person."""
        u = User(
            id=3,
            first_name="Bob",
            last_name="Lee",
            name=None,
            gender="M",
            email="bob@example.com",
            username="bob123",
            password="abc",
            role_id=3,
            is_active=False,
            created_at="2025-02-02"
        )
        self.assertEqual(u.gender, "M")
        self.assertEqual(u.email, "bob@example.com")


if __name__ == "__main__":
    unittest.main()
