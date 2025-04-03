import unittest
from src.grade_calculator import GradeCalculator


class TestGradeCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = GradeCalculator()

    # Tests for calculate_grade method
    def test_invalid_data_negative_points(self):
        self.assertEqual(self.calculator.calculate_grade(-10, 100), "Invalid data")

    def test_invalid_data_zero_max_points(self):
        self.assertEqual(self.calculator.calculate_grade(50, 0), "Invalid data")

    def test_grade_fail(self):
        self.assertEqual(self.calculator.calculate_grade(45, 100), "Fail")

    def test_grade_poor(self):
        self.assertEqual(self.calculator.calculate_grade(55, 100), "Poor")

    def test_grade_satisfactory(self):
        self.assertEqual(self.calculator.calculate_grade(70, 100), "Satisfactory")

    def test_grade_good(self):
        self.assertEqual(self.calculator.calculate_grade(85, 100), "Good")

    def test_grade_excellent(self):
        self.assertEqual(self.calculator.calculate_grade(95, 100), "Excellent")

    # Tests for has_passed method
    def test_has_passed_fail(self):
        self.assertFalse(self.calculator.has_passed("Fail"))

    def test_has_passed_invalid_data(self):
        self.assertFalse(self.calculator.has_passed("Invalid data"))

    def test_has_passed_positive_grade(self):
        self.assertTrue(self.calculator.has_passed("Poor"))
        self.assertTrue(self.calculator.has_passed("Satisfactory"))
        self.assertTrue(self.calculator.has_passed("Good"))
        self.assertTrue(self.calculator.has_passed("Excellent"))


if __name__ == '__main__':
    unittest.main()