"""
Loan approval system that evaluates applicants based on multiple criteria.
"""


class LoanApprover:
    """
    A class that determines loan approval based on credit score, income,
    debt-to-income ratio, and employment status.
    """

    def __init__(self):
        # Thresholds for decision making
        self.min_credit_score = 650
        self.min_income = 30000
        self.max_debt_ratio = 0.4  # 40% of income

    def approve_loan(self, credit_score, annual_income, existing_debt, is_employed):
        """
        Determines if a loan application should be approved, rejected, or referred for manual review.

        Args:
            credit_score (int): Applicant's credit score (300-850)
            annual_income (float): Applicant's annual income in dollars
            existing_debt (float): Applicant's existing debt in dollars
            is_employed (bool): Applicant's employment status

        Returns:
            str: 'Approved', 'Rejected', or 'Manual Review'
        """
        # Calculate debt-to-income ratio
        if annual_income == 0:
            debt_ratio = float('inf')  # Avoid division by zero
        else:
            debt_ratio = existing_debt / annual_income

        # Decision logic using multiple conditions
        if not is_employed:
            return "Rejected"  # Must be employed

        # High credit score case
        if credit_score >= 750:
            if debt_ratio <= self.max_debt_ratio:
                return "Approved"
            else:
                return "Manual Review"  # Good score but high debt

        # Medium credit score case
        elif credit_score >= self.min_credit_score:
            if annual_income >= self.min_income and debt_ratio <= self.max_debt_ratio:
                return "Approved"
            else:
                return "Manual Review"  # Decent score but other issues

        # Low credit score case
        else:
            if annual_income >= 2 * self.min_income and debt_ratio <= self.max_debt_ratio / 2:
                return "Manual Review"  # Poor score but excellent other factors
            else:
                return "Rejected"  # Poor score and other issues