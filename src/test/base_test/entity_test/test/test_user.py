import unittest
import os

# ===========================================================================
# PLACEHOLDERS (STUBS)
# ===========================================================================

from base_test.entity_test.user_test import User_test
from tools.mytools import MyTools

def create_user_test(
    uid,
    fname,
    lname,
    name,
    gender,
    email,
    username,
    password,
    role,
    active,
    created
):
    return User_test(
        id=uid,
        first_name=fname,
        last_name=lname,
        name=name,
        gender=gender,
        email=email,
        username=username,
        password=password,
        role_id=role,
        is_active=active,
        created_at=created
    )

def create_user_no_created_at():
    return User_test(
        id=100,
        first_name="Jane",
        last_name="Doe",
        name=None,
        gender="F",
        email="jane@example.com",
        username="jane123",
        password="pwd",
        role_id=1,
        is_active=True,
        created_at=None
    )

# ===========================================================================
# END PLACEHOLDERS
# ===========================================================================


class TestUserEntity(unittest.TestCase):

    def setUp(self):
        self.tmp = "temp_file.tmp"
        with open(self.tmp, "w") as f:
            f.write("x")

    def tearDown(self):
        if os.path.exists(self.tmp):
            os.remove(self.tmp)

    def test_initialization_fields(self):
        """Test that provided fields are assigned correctly."""
        u = create_user_test(
            uid=1,
            fname="Alice",
            lname="Smith",
            name=None,
            gender="F",
            email="alice@example.com",
            username="alice123",
            password="pw1",
            role=2,
            active=True,
            created="2025-01-01"
        )

        self.assertEqual(u.id, 1)
        self.assertEqual(u.first_name, "Alice")
        self.assertEqual(u.last_name, "Smith")
        self.assertEqual(u.username, "alice123")
        self.assertEqual(u.password, "pw1")
        self.assertEqual(u.role_id, 2)
        self.assertTrue(u.is_active)
        self.assertEqual(u.created_at, "2025-01-01")

    def test_created_at_auto_generated(self):
        """Test that created_at is auto-generated when None is provided."""
        u = create_user_no_created_at()
        self.assertIsNotNone(u.created_at)

    def test_inherited_person_fields(self):
        """Test that User inherits fields defined in Person."""
        u = create_user_test(
            uid=3,
            fname="Bob",
            lname="Lee",
            name=None,
            gender="M",
            email="bob@example.com",
            username="bob123",
            password="abc",
            role=3,
            active=False,
            created="2025-02-02"
        )

        self.assertEqual(u.gender, "M")
        self.assertEqual(u.email, "bob@example.com")

    def test_instance_type(self):
        """Test that the object is instance of User_test."""
        u = create_user_no_created_at()
        self.assertIsInstance(u, User_test)


if __name__ == "__main__":
    unittest.main()
