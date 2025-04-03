import unittest
import sys
import os

from src.discount_calculator import DiscountCalculator


class TestDiscountCalculatorBaseDiscount(unittest.TestCase):
    """
    Test cases for the base discount percentage calculation based on equivalence classes.

    Equivalence Classes for purchase amount:
    - EC1: amount < 0 (invalid input - should raise ValueError)
    - EC2: 0 <= amount < 100 (no discount)
    - EC3: 100 <= amount < 500 (5% discount)
    - EC4: 500 <= amount < 1000 (10% discount)
    - EC5: amount >= 1000 (15% discount)
    """

    def setUp(self):
        self.calculator = DiscountCalculator()

    def test_ec1_negative_amount(self):
        """EC1: Testing that negative amounts raise ValueError."""
        with self.assertRaises(ValueError):
            self.calculator.calculate_discount_percentage(-1)
        with self.assertRaises(ValueError):
            self.calculator.calculate_discount_percentage(-100)

    def test_ec2_zero_to_below_hundred(self):
        """EC2: Testing amounts from 0 to below 100 PLN (no discount)."""
        # Boundary value at the lower end
        self.assertEqual(self.calculator.calculate_discount_percentage(0), 0)

        # Middle value in the range
        self.assertEqual(self.calculator.calculate_discount_percentage(50), 0)

        # Boundary value at the upper end - epsilon
        self.assertEqual(self.calculator.calculate_discount_percentage(99.99), 0)

    def test_ec3_hundred_to_below_five_hundred(self):
        """EC3: Testing amounts from 100 to below 500 PLN (5% discount)."""
        # Boundary value at the lower end
        self.assertEqual(self.calculator.calculate_discount_percentage(100), 5)

        # Middle value in the range
        self.assertEqual(self.calculator.calculate_discount_percentage(250), 5)

        # Boundary value at the upper end - epsilon
        self.assertEqual(self.calculator.calculate_discount_percentage(499.99), 5)

    def test_ec4_five_hundred_to_below_thousand(self):
        """EC4: Testing amounts from 500 to below 1000 PLN (10% discount)."""
        # Boundary value at the lower end
        self.assertEqual(self.calculator.calculate_discount_percentage(500), 10)

        # Middle value in the range
        self.assertEqual(self.calculator.calculate_discount_percentage(750), 10)

        # Boundary value at the upper end - epsilon
        self.assertEqual(self.calculator.calculate_discount_percentage(999.99), 10)

    def test_ec5_thousand_and_above(self):
        """EC5: Testing amounts from 1000 PLN and above (15% discount)."""
        # Boundary value at the lower end
        self.assertEqual(self.calculator.calculate_discount_percentage(1000), 15)

        # Values above the boundary
        self.assertEqual(self.calculator.calculate_discount_percentage(1500), 15)
        self.assertEqual(self.calculator.calculate_discount_percentage(10000), 15)


class TestDiscountCalculatorFinalPrice(unittest.TestCase):
    """
    Test cases for the final price calculation with combined discounts.

    Additional Equivalence Classes for different_items_count:
    - EC6: different_items_count < 1 (invalid input - should raise ValueError)
    - EC7: 1 <= different_items_count < 5 (no additional discount)
    - EC8: different_items_count >= 5 (additional 1% discount)

    Boolean Equivalence Classes:
    - EC9: has_loyalty_card is True (additional 2% discount)
    - EC10: has_loyalty_card is False (no additional discount)
    - EC11: is_weekend is True (additional 1% discount)
    - EC12: is_weekend is False (no additional discount)
    """

    def setUp(self):
        self.calculator = DiscountCalculator()

    def test_ec6_invalid_items_count(self):
        """EC6: Testing that item count less than 1 raises ValueError."""
        with self.assertRaises(ValueError):
            self.calculator.calculate_final_price(100, different_items_count=0)
        with self.assertRaises(ValueError):
            self.calculator.calculate_final_price(100, different_items_count=-1)

    def test_ec7_no_item_discount(self):
        """EC7: Testing cases with 1 to 4 different items (no additional discount)."""
        # Base scenario: 100 PLN purchase (5% base discount) with 1 item
        self.assertEqual(self.calculator.calculate_final_price(100, different_items_count=1), 95)

        # Same purchase with 4 items (still only 5% discount)
        self.assertEqual(self.calculator.calculate_final_price(100, different_items_count=4), 95)

    def test_ec8_item_discount(self):
        """EC8: Testing cases with 5 or more different items (additional 1% discount)."""
        # Boundary case: 100 PLN purchase with exactly 5 items (5% base + 1% item discount)
        self.assertEqual(self.calculator.calculate_final_price(100, different_items_count=5), 94)

        # Similar case with more items (same discount)
        self.assertEqual(self.calculator.calculate_final_price(100, different_items_count=10), 94)

    def test_ec9_ec10_loyalty_card(self):
        """EC9, EC10: Testing effect of loyalty card on final price."""
        # No loyalty card case
        self.assertEqual(self.calculator.calculate_final_price(100, has_loyalty_card=False), 95)

        # With loyalty card (additional 2% discount)
        self.assertEqual(self.calculator.calculate_final_price(100, has_loyalty_card=True), 93)

    def test_ec11_ec12_weekend_discount(self):
        """EC11, EC12: Testing effect of weekend purchase on final price."""
        # Weekday purchase
        self.assertEqual(self.calculator.calculate_final_price(100, is_weekend=False), 95)

        # Weekend purchase (additional 1% discount)
        self.assertEqual(self.calculator.calculate_final_price(100, is_weekend=True), 94)

    def test_combined_discounts(self):
        """Testing combinations of different discount factors."""
        # 1000 PLN purchase (15% base discount) with all additional discounts
        # 15% + 2% (loyalty) + 1% (items) + 1% (weekend) = 19% total
        # 1000 - (1000 * 0.19) = 810
        self.assertEqual(
            self.calculator.calculate_final_price(
                1000, has_loyalty_card=True, different_items_count=5, is_weekend=True
            ),
            810
        )

        # 600 PLN purchase (10% base discount) with mixed additional discounts
        # 10% + 2% (loyalty) + 0% (not enough items) + 1% (weekend) = 13% total
        # 600 - (600 * 0.13) = 522
        self.assertEqual(
            self.calculator.calculate_final_price(
                600, has_loyalty_card=True, different_items_count=3, is_weekend=True
            ),
            522
        )

        # 50 PLN purchase (0% base discount) with all additional discounts
        # 0% + 2% (loyalty) + 1% (items) + 1% (weekend) = 4% total
        # 50 - (50 * 0.04) = 48
        self.assertEqual(
            self.calculator.calculate_final_price(
                50, has_loyalty_card=True, different_items_count=5, is_weekend=True
            ),
            48
        )


if __name__ == '__main__':
    unittest.main()