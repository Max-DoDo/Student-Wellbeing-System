import unittest
from base.entity.person import Person

class TestPersonEntity(unittest.TestCase):

    def test_name_construction(self):
        """Test that name is constructed from first and last name when not provided."""
        p = Person(
            id=1,
            first_name="John",
            last_name="Doe",
            name=None,
            gender="M",
            email="johndoe@email.com"
        )
        self.assertEqual(p.name, "John Doe")

    def test_split_name_into_parts(self):
        """Test splitting full name into first_name and last_name."""
        p = Person(
            id=2,
            first_name="",
            last_name="",
            name="Alice Wonderland",
            gender="F",
            email="alice@uni.com"
        )
        self.assertEqual(p.first_name, "Alice")
        self.assertEqual(p.last_name, "Wonderland")

if __name__ == "__main__":
    unittest.main()
