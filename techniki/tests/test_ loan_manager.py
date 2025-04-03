import unittest
import sys
import os
from datetime import datetime

# Add the src directory to the path so we can import our module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.loan_manager import LoanManager


class TestLoanPeriodBoundaryValues(unittest.TestCase):
    """
    Tests for loan period validation using boundary value analysis.

    This demonstrates one-point, two-point, and three-point boundary value testing
    approaches for the validate_loan_days method.
    """

    def setUp(self):
        self.loan_manager = LoanManager()

    def test_regular_book_loan_period_one_point(self):
        """
        One-point boundary value tests for regular book loan period.

        For one-point boundary testing, we only test exactly at the boundary values.
        For regular books, the valid range is 14-30 days, so we test 14 and 30 days.
        """
        # At minimum boundary (14 days)
        self.assertTrue(
            self.loan_manager.validate_loan_days(
                LoanManager.REGULAR_BOOK, 14
            ),
            "Should allow exactly 14 days for a regular book"
        )

        # At maximum boundary (30 days)
        self.assertTrue(
            self.loan_manager.validate_loan_days(
                LoanManager.REGULAR_BOOK, 30
            ),
            "Should allow exactly 30 days for a regular book"
        )

    def test_popular_book_loan_period_two_point(self):
        """
        Two-point boundary value tests for popular book loan period.

        For two-point boundary testing, we test exactly at the boundary and just outside
        the boundary (boundary ± 1). For popular books, the valid range is 7-14 days.
        """
        # Minimum boundary tests (7 days)
        self.assertFalse(
            self.loan_manager.validate_loan_days(
                LoanManager.POPULAR_BOOK, 6
            ),
            "Should not allow 6 days for a popular book (below min)"
        )

        self.assertTrue(
            self.loan_manager.validate_loan_days(
                LoanManager.POPULAR_BOOK, 7
            ),
            "Should allow exactly 7 days for a popular book (at min)"
        )

        # Maximum boundary tests (14 days)
        self.assertTrue(
            self.loan_manager.validate_loan_days(
                LoanManager.POPULAR_BOOK, 14
            ),
            "Should allow exactly 14 days for a popular book (at max)"
        )

        self.assertFalse(
            self.loan_manager.validate_loan_days(
                LoanManager.POPULAR_BOOK, 15
            ),
            "Should not allow 15 days for a popular book (above max)"
        )

    def test_reference_book_loan_period_three_point(self):
        """
        Three-point boundary value tests for reference book loan period.

        For three-point boundary testing, we test at the boundary, just outside the boundary,
        and one more value outside (boundary ± 1 and boundary ± 2).
        For reference books, the valid range is 1-3 days.
        """
        # Minimum boundary tests (1 day)
        self.assertFalse(
            self.loan_manager.validate_loan_days(
                LoanManager.REFERENCE_BOOK, -1
            ),
            "Should not allow -1 days for a reference book (well below min)"
        )

        self.assertFalse(
            self.loan_manager.validate_loan_days(
                LoanManager.REFERENCE_BOOK, 0
            ),
            "Should not allow 0 days for a reference book (just below min)"
        )

        self.assertTrue(
            self.loan_manager.validate_loan_days(
                LoanManager.REFERENCE_BOOK, 1
            ),
            "Should allow exactly 1 day for a reference book (at min)"
        )

        # Maximum boundary tests (3 days)
        self.assertTrue(
            self.loan_manager.validate_loan_days(
                LoanManager.REFERENCE_BOOK, 3
            ),
            "Should allow exactly 3 days for a reference book (at max)"
        )

        self.assertFalse(
            self.loan_manager.validate_loan_days(
                LoanManager.REFERENCE_BOOK, 4
            ),
            "Should not allow 4 days for a reference book (just above max)"
        )

        self.assertFalse(
            self.loan_manager.validate_loan_days(
                LoanManager.REFERENCE_BOOK, 5
            ),
            "Should not allow 5 days for a reference book (well above max)"
        )


class TestBookQuantityBoundaryValues(unittest.TestCase):
    """
    Tests for book quantity validation using boundary value analysis.

    This demonstrates boundary value testing approaches for the validate_book_quantity method.
    """

    def setUp(self):
        self.loan_manager = LoanManager()

    def test_regular_user_quantity_one_point(self):
        """One-point boundary value tests for regular user book quantity (max 5 books)."""
        # Test with 0 current books, borrowing 5 more (at exactly max)
        self.assertTrue(
            self.loan_manager.validate_book_quantity(
                LoanManager.REGULAR_USER, 0, 5
            ),
            "Regular user with 0 books should be able to borrow exactly 5 more"
        )

        # Test with 5 current books, borrowing 0 more (at exactly max)
        self.assertTrue(
            self.loan_manager.validate_book_quantity(
                LoanManager.REGULAR_USER, 5, 0
            ),
            "Regular user with 5 books should be able to borrow 0 more"
        )

    def test_premium_user_quantity_two_point(self):
        """Two-point boundary value tests for premium user book quantity (max 10 books)."""
        # Test with 9 current books

        self.assertTrue(
            self.loan_manager.validate_book_quantity(
                LoanManager.PREMIUM_USER, 9, 1
            ),
            "Premium user with 9 books should be able to borrow 1 more (at max)"
        )

        self.assertFalse(
            self.loan_manager.validate_book_quantity(
                LoanManager.PREMIUM_USER, 9, 2
            ),
            "Premium user with 9 books should not be able to borrow 2 more (above max)"
        )

        # Test with 10 current books
        self.assertTrue(
            self.loan_manager.validate_book_quantity(
                LoanManager.PREMIUM_USER, 10, 0
            ),
            "Premium user with 10 books should be able to borrow 0 more (at max)"
        )

        self.assertFalse(
            self.loan_manager.validate_book_quantity(
                LoanManager.PREMIUM_USER, 10, 1
            ),
            "Premium user with 10 books should not be able to borrow 1 more (above max)"
        )

    def test_researcher_user_quantity_three_point(self):
        """Three-point boundary value tests for researcher user book quantity (max 15 books)."""
        # Testing at lower boundaries (0 books)
        with self.assertRaises(ValueError):
            self.loan_manager.validate_book_quantity(
                LoanManager.RESEARCHER_USER, 0, -1
            )

        with self.assertRaises(ValueError):
            self.loan_manager.validate_book_quantity(
                LoanManager.RESEARCHER_USER, 0, 0
            )

        self.assertTrue(
            self.loan_manager.validate_book_quantity(
                LoanManager.RESEARCHER_USER, 0, 1
            ),
            "Researcher user with 0 books should be able to borrow 1 more"
        )

        # Testing at upper boundaries (13-15 books)
        self.assertTrue(
            self.loan_manager.validate_book_quantity(
                LoanManager.RESEARCHER_USER, 13, 2
            ),
            "Researcher user with 13 books should be able to borrow 2 more (at max)"
        )

        self.assertTrue(
            self.loan_manager.validate_book_quantity(
                LoanManager.RESEARCHER_USER, 14, 1
            ),
            "Researcher user with 14 books should be able to borrow 1 more (at max)"
        )

        self.assertFalse(
            self.loan_manager.validate_book_quantity(
                LoanManager.RESEARCHER_USER, 14, 2
            ),
            "Researcher user with 14 books should not be able to borrow 2 more (above max)"
        )

        self.assertTrue(
            self.loan_manager.validate_book_quantity(
                LoanManager.RESEARCHER_USER, 15, 0
            ),
            "Researcher user with 15 books should be able to borrow 0 more (at max)"
        )

        self.assertFalse(
            self.loan_manager.validate_book_quantity(
                LoanManager.RESEARCHER_USER, 15, 1
            ),
            "Researcher user with 15 books should not be able to borrow 1 more (above max)"
        )

        self.assertFalse(
            self.loan_manager.validate_book_quantity(
                LoanManager.RESEARCHER_USER, 16, 0
            ),
            "Researcher user with 16 books is already above max"
        )


class TestLoanRenewalBoundaryValues(unittest.TestCase):
    """
    Tests for loan renewal validation using boundary value analysis.

    This demonstrates boundary value testing for the can_renew_loan method.
    """

    def setUp(self):
        self.loan_manager = LoanManager()

    def test_renewal_count_boundaries(self):
        """Testing boundary values for the number of previous renewals (max is 2)."""
        # Using a regular book with plenty of loan days left to isolate renewal count testing

        # At boundary (2 previous renewals)
        self.assertFalse(
            self.loan_manager.can_renew_loan(
                LoanManager.REGULAR_BOOK, 10, 5, previous_renewals=2
            ),
            "Should not allow renewal with exactly 2 previous renewals"
        )

        # Just below boundary (1 previous renewal)
        self.assertTrue(
            self.loan_manager.can_renew_loan(
                LoanManager.REGULAR_BOOK, 10, 5, previous_renewals=1
            ),
            "Should allow renewal with 1 previous renewal"
        )

        # Just above boundary (3 previous renewals)
        self.assertFalse(
            self.loan_manager.can_renew_loan(
                LoanManager.REGULAR_BOOK, 10, 5, previous_renewals=3
            ),
            "Should not allow renewal with 3 previous renewals"
        )

    def test_total_loan_period_boundaries(self):
        """
        Testing boundary values for the total loan period.

        For a regular book (max 30 days), we'll test combinations of current loan duration
        and requested renewal days that approach the 30-day boundary.
        """
        # At boundary: 25 days already loaned + 5 days renewal = 30 days total (allowed)
        self.assertTrue(
            self.loan_manager.can_renew_loan(
                LoanManager.REGULAR_BOOK, 25, 5
            ),
            "Should allow renewal when total is exactly at max (30 days)"
        )

        # Just over boundary: 25 days already loaned + 6 days renewal = 31 days total (not allowed)
        self.assertFalse(
            self.loan_manager.can_renew_loan(
                LoanManager.REGULAR_BOOK, 25, 6
            ),
            "Should not allow renewal when total exceeds max (31 days)"
        )

        # Just under boundary: 24 days already loaned + 6 days renewal = 30 days total (allowed)
        self.assertTrue(
            self.loan_manager.can_renew_loan(
                LoanManager.REGULAR_BOOK, 24, 6
            ),
            "Should allow renewal when total is exactly at max (30 days)"
        )

    def test_combined_boundary_conditions(self):
        """Testing combinations of boundary conditions for renewals."""
        # Case 1: At max renewals (2) but loan period would be ok
        self.assertFalse(
            self.loan_manager.can_renew_loan(
                LoanManager.REGULAR_BOOK, 15, 5, previous_renewals=2
            ),
            "Should not allow renewal when at max renewals, even if period is ok"
        )

        # Case 2: Below max renewals (1) but loan period would exceed max
        self.assertFalse(
            self.loan_manager.can_renew_loan(
                LoanManager.REGULAR_BOOK, 28, 3, previous_renewals=1
            ),
            "Should not allow renewal when period would exceed max, even if renewals are ok"
        )

        # Case 3: Below max renewals (1) and loan period would be at boundary (30 days)
        self.assertTrue(
            self.loan_manager.can_renew_loan(
                LoanManager.REGULAR_BOOK, 27, 3, previous_renewals=1
            ),
            "Should allow renewal when renewals and period are both ok"
        )

        # Case 4: Book is requested by another user (this overrides all other conditions)
        self.assertFalse(
            self.loan_manager.can_renew_loan(
                LoanManager.REGULAR_BOOK, 15, 5, previous_renewals=0, is_requested=True
            ),
            "Should not allow renewal when book is requested, regardless of other conditions"
        )


class TestCalculateFinesBoundaryValues(unittest.TestCase):
    """
    Tests for fine calculation using boundary value analysis.

    This demonstrates boundary value testing for the calculate_fine method.
    """

    def setUp(self):
        self.loan_manager = LoanManager()

    def test_zero_days_overdue(self):
        """Testing at the boundary of 0 days overdue."""
        self.assertEqual(
            self.loan_manager.calculate_fine(0, LoanManager.REGULAR_BOOK),
            0.0,
            "Fine should be 0 for exactly 0 days overdue"
        )

        self.assertEqual(
            self.loan_manager.calculate_fine(-1, LoanManager.REGULAR_BOOK),
            0.0,
            "Fine should be 0 for negative days overdue"
        )

    def test_max_fine_boundaries(self):
        """
        Testing at the boundaries of maximum fine.
        Maximum fine is 10x the daily rate.
        """
        # For regular books (0.50 PLN per day, max 5.00 PLN)

        # Just below max (9 days = 4.50 PLN)
        self.assertEqual(
            self.loan_manager.calculate_fine(9, LoanManager.REGULAR_BOOK),
            4.50,
            "Fine should be 4.50 PLN for 9 days (below max)"
        )

        # At max (10 days = 5.00 PLN)
        self.assertEqual(
            self.loan_manager.calculate_fine(10, LoanManager.REGULAR_BOOK),
            5.00,
            "Fine should be 5.00 PLN for 10 days (at max)"
        )

        # Above max (11 days would be 5.50 PLN, but capped at 5.00 PLN)
        self.assertEqual(
            self.loan_manager.calculate_fine(11, LoanManager.REGULAR_BOOK),
            5.00,
            "Fine should be capped at 5.00 PLN for 11 days (above max)"
        )

        # Well above max (20 days would be 10.00 PLN, but capped at 5.00 PLN)
        self.assertEqual(
            self.loan_manager.calculate_fine(20, LoanManager.REGULAR_BOOK),
            5.00,
            "Fine should be capped at 5.00 PLN for 20 days (well above max)"
        )

    def test_different_book_types(self):
        """Testing fine calculation for different book types at their cap boundaries."""
        # Regular books (0.50 PLN per day, max 5.00 PLN)
        self.assertEqual(
            self.loan_manager.calculate_fine(10, LoanManager.REGULAR_BOOK),
            5.00,
            "Max fine for regular books should be 5.00 PLN"
        )

        # Popular books (1.00 PLN per day, max 10.00 PLN)
        self.assertEqual(
            self.loan_manager.calculate_fine(10, LoanManager.POPULAR_BOOK),
            10.00,
            "Max fine for popular books should be 10.00 PLN"
        )

        # Reference books (2.00 PLN per day, max 20.00 PLN)
        self.assertEqual(
            self.loan_manager.calculate_fine(10, LoanManager.REFERENCE_BOOK),
            20.00,
            "Max fine for reference books should be 20.00 PLN"
        )


if __name__ == '__main__':
    unittest.main()