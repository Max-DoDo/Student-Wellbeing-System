import unittest
import os

# ===========================================================================
# PLACEHOLDERS (STUBS)
# ===========================================================================

from base_test.entity_test.student_test import Student_test

def create_student_test(
        sid,
        fname,
        lname,
        name,
        gender,
        email,
        tutor,
        emergency_name,
        emergency_phone
    ):
    return Student_test(
        id=sid,
        first_name=fname,
        last_name=lname,
        name=name,
        gender=gender,
        email=email,
        personal_tutor_email=tutor,
        emergency_contact_name=emergency_name,
        emergency_contact_phone=emergency_phone
    )

def create_student_minimal():
    return Student_test(
        id=10,
        first_name="John",
        last_name="Doe",
        name=None,
        gender="M",
        email="john@uni.com"
    )

# ===========================================================================
# END PLACEHOLDERS
# ===========================================================================


class TestStudentEntity(unittest.TestCase):

    def setUp(self):
        self.tmp = "temp_file.tmp"
        with open(self.tmp, "w") as f:
            f.write("x")

    def tearDown(self):
        if os.path.exists(self.tmp):
            os.remove(self.tmp)

    def test_basic_initialization(self):
        """Test that provided field values are assigned correctly."""
        s = create_student_test(
            sid=1,
            fname="Alice",
            lname="Smith",
            name=None,
            gender="F",
            email="alice@uni.com",
            tutor="tutor@uni.com",
            emergency_name="Mom",
            emergency_phone="123456"
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
        s = create_student_minimal()

        self.assertEqual(s.name, "John Doe")

    def test_inherited_fields(self):
        """Test that Student inherits fields from Person."""
        s = create_student_test(
            sid=3,
            fname="Bob",
            lname="Lee",
            name=None,
            gender="M",
            email="bob@uni.com",
            tutor="tutor@uni.com",
            emergency_name="Dad",
            emergency_phone="789000"
        )

        self.assertEqual(s.gender, "M")
        self.assertEqual(s.email, "bob@uni.com")

    def test_instance_type(self):
        """Test that the object is instance of Student_test."""
        s = create_student_minimal()
        self.assertIsInstance(s, Student_test)


if __name__ == "__main__":
    unittest.main()
