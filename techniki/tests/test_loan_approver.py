"""
Tests for the LoanApprover class using decision table testing approach.

Decision table testing allows us to systematically test combinations of inputs
and their expected outcomes. This is particularly useful for complex business logic
with multiple conditions.
"""

import unittest
import sys
import os

# Add the src directory to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.loan_approver import LoanApprover


class TestLoanApproverDecisionTable(unittest.TestCase):
    """
    Test case for the LoanApprover using decision table testing.

    Decision table:
    +----------------+--------+--------+--------+--------+--------+--------+--------+--------+
    | Test Case #    | 1      | 2      | 3      | 4      | 5      | 6      | 7      | 8      |
    +----------------+--------+--------+--------+--------+--------+--------+--------+--------+
    | Is Employed    | Y      | Y      | Y      | Y      | Y      | Y      | Y      | N      |
    | Credit Score   | High   | High   | Med    | Med    | Med    | Low    | Low    | Any    |
    | Income         | Any    | Any    | High   | High   | Low    | V.High | Other  | Any    |
    | Debt Ratio     | Low    | High   | Low    | High   | Any    | V.Low  | Any    | Any    |
    +----------------+--------+--------+--------+--------+--------+--------+--------+--------+
    | Expected       | Appr.  | Manual | Appr.  | Manual | Manual | Manual | Reject | Reject |
    +----------------+--------+--------+--------+--------+--------+--------+--------+--------+
    """

    def setUp(self):
        """Initialize the LoanApprover instance for each test."""
        self.approver = LoanApprover()

        # Define test values based on the thresholds in the LoanApprover
        # Credit score categories
        self.high_credit = 780  # High: >= 750
        self.medium_credit = 700  # Medium: 650-749
        self.low_credit = 600  # Low: < 650

        # Income categories
        self.very_high_income = 70000  # Very high: >= 2 * minimum
        self.high_income = 50000  # High: >= minimum
        self.low_income = 20000  # Low: < minimum

        # Debt ratio categories (based on income)
        self.very_low_debt_ratio = 0.15  # Very low: <= max/2
        self.low_debt_ratio = 0.3  # Low: <= max
        self.high_debt_ratio = 0.5  # High: > max

    def test_case_1_high_credit_low_debt(self):
        """Test Case 1: Employed, high credit score, any income, low debt ratio -> Approved."""
        result = self.approver.approve_loan(
            credit_score=self.high_credit,
            annual_income=self.high_income,  # Any income is acceptable here
            existing_debt=self.high_income * self.low_debt_ratio,
            is_employed=True
        )
        self.assertEqual(result, "Approved")

    def test_case_2_high_credit_high_debt(self):
        """Test Case 2: Employed, high credit score, any income, high debt ratio -> Manual Review."""
        result = self.approver.approve_loan(
            credit_score=self.high_credit,
            annual_income=self.high_income,  # Any income is acceptable here
            existing_debt=self.high_income * self.high_debt_ratio,
            is_employed=True
        )
        self.assertEqual(result, "Manual Review")

    def test_case_3_medium_credit_high_income_low_debt(self):
        """Test Case 3: Employed, medium credit score, high income, low debt ratio -> Approved."""
        result = self.approver.approve_loan(
            credit_score=self.medium_credit,
            annual_income=self.high_income,
            existing_debt=self.high_income * self.low_debt_ratio,
            is_employed=True
        )
        self.assertEqual(result, "Approved")

    def test_case_4_medium_credit_high_income_high_debt(self):
        """Test Case 4: Employed, medium credit score, high income, high debt ratio -> Manual Review."""
        result = self.approver.approve_loan(
            credit_score=self.medium_credit,
            annual_income=self.high_income,
            existing_debt=self.high_income * self.high_debt_ratio,
            is_employed=True
        )
        self.assertEqual(result, "Manual Review")

    def test_case_5_medium_credit_low_income(self):
        """Test Case 5: Employed, medium credit score, low income, any debt ratio -> Manual Review."""
        result = self.approver.approve_loan(
            credit_score=self.medium_credit,
            annual_income=self.low_income,
            existing_debt=self.low_income * self.low_debt_ratio,  # Even low debt ratio doesn't help
            is_employed=True
        )
        self.assertEqual(result, "Manual Review")

    def test_case_6_low_credit_very_high_income_very_low_debt(self):
        """Test Case 6: Employed, low credit score, very high income, very low debt ratio -> Manual Review."""
        result = self.approver.approve_loan(
            credit_score=self.low_credit,
            annual_income=self.very_high_income,
            existing_debt=self.very_high_income * self.very_low_debt_ratio,
            is_employed=True
        )
        self.assertEqual(result, "Manual Review")

    def test_case_7_low_credit_other_conditions(self):
        """Test Case 7: Employed, low credit score, not meeting special conditions -> Rejected."""
        result = self.approver.approve_loan(
            credit_score=self.low_credit,
            annual_income=self.high_income,  # Not very high
            existing_debt=self.high_income * self.low_debt_ratio,  # Not very low
            is_employed=True
        )
        self.assertEqual(result, "Rejected")

    def test_case_8_unemployed(self):
        """Test Case 8: Unemployed, any other conditions -> Rejected."""
        result = self.approver.approve_loan(
            credit_score=self.high_credit,  # Even with perfect other conditions
            annual_income=self.very_high_income,
            existing_debt=self.very_high_income * self.very_low_debt_ratio,
            is_employed=False
        )
        self.assertEqual(result, "Rejected")

    def test_edge_cases(self):
        """Test edge cases not covered in the main decision table."""
        # Zero income edge case
        result = self.approver.approve_loan(
            credit_score=self.high_credit,
            annual_income=0,
            existing_debt=5000,
            is_employed=True
        )
        self.assertEqual(result, "Manual Review", "Zero income should lead to Manual Review")

        # Exactly at threshold values
        result = self.approver.approve_loan(
            credit_score=self.approver.min_credit_score,  # Exactly 650
            annual_income=self.approver.min_income,  # Exactly 30000
            existing_debt=self.approver.min_income * self.approver.max_debt_ratio,  # Exactly at max ratio
            is_employed=True
        )
        self.assertEqual(result, "Approved", "Threshold values should be approved")


if __name__ == '__main__':
    unittest.main()