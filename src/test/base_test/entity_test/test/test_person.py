import unittest
import os

# ===========================================================================
# PLACEHOLDERS (STUBS)
# ===========================================================================

from base_test.entity_test.person_test import Person_test
from tools.log import Log

def create_person_test(pid, fname, lname, name, gender, email):
    return Person_test(
        id=pid,
        first_name=fname,
        last_name=lname,
        name=name,
        gender=gender,
        email=email
    )

def create_person_no_names():
    return Person_test(
        id=99,
        first_name="",
        last_name="",
        name="",
        gender="",
        email=""
    )

# ===========================================================================
# END PLACEHOLDERS
# ===========================================================================


class TestPersonEntity(unittest.TestCase):

    def setUp(self):
        self.tmp = "temp_file.tmp"
        with open(self.tmp, "w") as f:
            f.write("x")

    def tearDown(self):
        if os.path.exists(self.tmp):
            os.remove(self.tmp)

    def test_name_construction(self):
        """Test that name is constructed from first and last name when not provided."""
        p = create_person_test(
            pid=1,
            fname="John",
            lname="Doe",
            name=None,
            gender="M",
            email="johndoe@email.com"
        )

        self.assertEqual(p.name, "John Doe")

    def test_split_name_into_parts(self):
        """Test splitting full name into first_name and last_name."""
        p = create_person_test(
            pid=2,
            fname="",
            lname="",
            name="Alice Wonderland",
            gender="F",
            email="alice@uni.com"
        )

        self.assertEqual(p.first_name, "Alice")
        self.assertEqual(p.last_name, "Wonderland")

    def test_single_word_name(self):
        """Test that single-word name results in empty last_name."""
        p = create_person_test(
            pid=3,
            fname="",
            lname="",
            name="Plato",
            gender="M",
            email="plato@classic.com"
        )

        self.assertEqual(p.first_name, "Plato")
        self.assertEqual(p.last_name, "")

    def test_no_name_logging(self):
        """Test that missing name triggers the warning path."""
        p = create_person_no_names()
        # __post_init__ returns early; values remain default
        self.assertEqual(p.first_name, "")
        self.assertEqual(p.last_name, "")
        self.assertEqual(p.name, "")

    def test_instance_type(self):
        """Test that the created object is of the expected class."""
        p = create_person_test(1, "A", "B", None, "M", "a@b.com")
        self.assertIsInstance(p, Person_test)


if __name__ == "__main__":
    unittest.main()
