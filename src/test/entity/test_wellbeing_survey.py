import unittest
from base.entity.wellbeing_survey import Wellbeing_Survey # Use the real Wellbeing_Survey entity

class TestWellbeingSurveyEntity(unittest.TestCase):

    def test_field_initialization(self):
        """Test that provided values are assigned to fields correctly."""
        s = Wellbeing_Survey(
            survey_id=1,
            student_id=5,
            week_number=2,
            stress_level=3,
            hours_slept=8,
            survey_date="2025-01-01"
        )
        self.assertEqual(s.survey_id, 1)
        self.assertEqual(s.student_id, 5)
        self.assertEqual(s.week_number, 2)
        self.assertEqual(s.stress_level, 3)
        self.assertEqual(s.hours_slept, 8)
        self.assertEqual(s.survey_date, "2025-01-01")

    def test_auto_date_assignment(self):
        """Test that survey_date is auto-generated when None is provided."""
        s = Wellbeing_Survey(
            survey_id=10,
            student_id=20,
            week_number=3,
            stress_level=4,
            hours_slept=7,
            survey_date=None
        )
        self.assertIsNotNone(s.survey_date)


if __name__ == "__main__":
    unittest.main()
