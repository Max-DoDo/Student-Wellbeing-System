import unittest
import os

# ===========================================================================
# PLACEHOLDERS (STUBS)
# ===========================================================================

from base_test.entity_test.wellbeing_survey_test import Wellbeing_Survey_test

def create_survey_test(
    sid,
    student,
    week,
    stress,
    sleep,
    date
):
    return Wellbeing_Survey_test(
        survey_id=sid,
        student_id=student,
        week_number=week,
        stress_level=stress,
        hours_slept=sleep,
        survey_date=date
    )

def create_survey_none_date():
    return Wellbeing_Survey_test(
        survey_id=10,
        student_id=20,
        week_number=3,
        stress_level=4,
        hours_slept=7,
        survey_date=None
    )

# ===========================================================================
# END PLACEHOLDERS
# ===========================================================================


class TestWellbeingSurveyEntity(unittest.TestCase):

    def setUp(self):
        self.tmp = "temp_file.tmp"
        with open(self.tmp, "w") as f:
            f.write("x")

    def tearDown(self):
        if os.path.exists(self.tmp):
            os.remove(self.tmp)

    def test_field_initialization(self):
        """Test that provided values are assigned to fields correctly."""
        s = create_survey_test(
            sid=1,
            student=5,
            week=2,
            stress=3,
            sleep=8,
            date="2025-01-01"
        )

        self.assertEqual(s.survey_id, 1)
        self.assertEqual(s.student_id, 5)
        self.assertEqual(s.week_number, 2)
        self.assertEqual(s.stress_level, 3)
        self.assertEqual(s.hours_slept, 8)
        self.assertEqual(s.survey_date, "2025-01-01")

    def test_auto_date_assignment(self):
        """Test that survey_date is auto-generated when None is provided."""
        s = create_survey_none_date()
        self.assertIsNotNone(s.survey_date)

    def test_instance_type(self):
        """Test that the object is instance of Wellbeing_Survey_test."""
        s = create_survey_test(1, 2, 1, 4, 7, "2025-02-02")
        self.assertIsInstance(s, Wellbeing_Survey_test)


if __name__ == "__main__":
    unittest.main()
