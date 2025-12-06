import unittest
from base.entity.student import Student # Use the real Student entity

class TestStudentEntity(unittest.TestCase):

    def test_basic_initialization(self):
        """Test that provided field values are assigned correctly."""
        s = Student(
            id=1,
            first_name="Alice",
            last_name="Smith",
            name=None,
            gender="F",
            email="alice@uni.com",
            personal_tutor_email="tutor@uni.com",
            emergency_contact_name="Mom",
            emergency_contact_phone="123456"
        )
        self.assertEqual(s.id, 1)
        self.assertEqual(s.first_name, "Alice")
        self.assertEqual(s.last_name, "Smith")
        self.assertEqual(s.email, "alice@uni.com")
        self.assertEqual(s.personal_tutor_email, "tutor@uni.com")
        self.assertEqual(s.emergency_contact_name, "Mom")
        self.assertEqual(s.emergency_contact_phone, "123456")

    def test_name_auto_construction(self):
        """Test that name is auto-built from first and last name when missing."""
        s = Student(
            id=10,
            first_name="John",
            last_name="Doe",
            name=None,
            gender="M",
            email="john@uni.com",
            personal_tutor_email="tutor@uni.com"
        )
        self.assertEqual(s.name, "John Doe")

    def test_inherited_fields(self):
        """Test that Student inherits fields from Person."""
        s = Student(
            id=3,
            first_name="Bob",
            last_name="Lee",
            name=None,
            gender="M",
            email="bob@uni.com",
            personal_tutor_email="tutor@uni.com",
            emergency_contact_name="Dad",
            emergency_contact_phone="789000"
        )
        self.assertEqual(s.gender, "M")
        self.assertEqual(s.email, "bob@uni.com")


if __name__ == "__main__":
    unittest.main()
