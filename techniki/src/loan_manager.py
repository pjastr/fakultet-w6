from datetime import datetime, timedelta


class LoanManager:
    """
    Manages library book loans with different rules based on book type and user status.

    Loan periods:
    - Regular books: 14-30 days (inclusive)
    - Popular/new books: 7-14 days (inclusive)
    - Reference books: 1-3 days (inclusive)

    Users can borrow:
    - Regular users: 1-5 books (inclusive)
    - Premium users: 1-10 books (inclusive)
    - Researcher users: 1-15 books (inclusive)

    Renewal rules:
    - Can't renew if days_already_loaned + renewal_days exceeds max loan period for book type
    - Can't renew if number of previous renewals >= 2
    - Can't renew if book has been requested by another user
    """

    # Book type constants
    REGULAR_BOOK = "regular"
    POPULAR_BOOK = "popular"
    REFERENCE_BOOK = "reference"

    # User type constants
    REGULAR_USER = "regular"
    PREMIUM_USER = "premium"
    RESEARCHER_USER = "researcher"

    # Loan period constraints (in days)
    LOAN_PERIODS = {
        REGULAR_BOOK: {"min": 14, "max": 30},
        POPULAR_BOOK: {"min": 7, "max": 14},
        REFERENCE_BOOK: {"min": 1, "max": 3}
    }

    # Book quantity constraints
    MAX_BOOKS = {
        REGULAR_USER: 5,
        PREMIUM_USER: 10,
        RESEARCHER_USER: 15
    }

    # Maximum allowed renewals
    MAX_RENEWALS = 2

    def validate_loan_days(self, book_type, loan_days):
        """Validates if the requested loan period is within allowed range for book type."""
        if book_type not in self.LOAN_PERIODS:
            raise ValueError(f"Unknown book type: {book_type}")

        min_days = self.LOAN_PERIODS[book_type]["min"]
        max_days = self.LOAN_PERIODS[book_type]["max"]

        if loan_days < min_days or loan_days > max_days:
            return False
        return True

    def validate_book_quantity(self, user_type, current_borrowed, additional_books=1):
        """
        Validates if user can borrow additional books.

        Args:
            user_type: Type of user (regular, premium, researcher)
            current_borrowed: Number of books currently borrowed by user
            additional_books: Number of new books user wants to borrow

        Returns:
            bool: True if borrowing is allowed, False otherwise
        """
        if user_type not in self.MAX_BOOKS:
            raise ValueError(f"Unknown user type: {user_type}")

        if current_borrowed < 0:
            raise ValueError("Current borrowed books cannot be negative")

        if additional_books <= 0:
            raise ValueError("Additional books must be positive")

        max_allowed = self.MAX_BOOKS[user_type]

        # Check if total would exceed limit
        if current_borrowed + additional_books > max_allowed:
            return False
        return True

    def can_renew_loan(self, book_type, days_already_loaned, renewal_days,
                       previous_renewals=0, is_requested=False):
        """
        Determines if a book loan can be renewed.

        Args:
            book_type: Type of book
            days_already_loaned: How many days book has been loaned
            renewal_days: How many additional days requested
            previous_renewals: How many times loan has been renewed before
            is_requested: Whether another user has requested this book

        Returns:
            bool: True if renewal is allowed, False otherwise
        """
        if book_type not in self.LOAN_PERIODS:
            raise ValueError(f"Unknown book type: {book_type}")

        if days_already_loaned < 0:
            raise ValueError("Days already loaned cannot be negative")

        if renewal_days <= 0:
            raise ValueError("Renewal days must be positive")

        if previous_renewals < 0:
            raise ValueError("Previous renewals cannot be negative")

        # Check if another user requested the book
        if is_requested:
            return False

        # Check max renewals
        if previous_renewals >= self.MAX_RENEWALS:
            return False

        # Check if total loan period would exceed maximum
        max_days = self.LOAN_PERIODS[book_type]["max"]
        if days_already_loaned + renewal_days > max_days:
            return False

        return True

    def calculate_due_date(self, loan_date, loan_days):
        """Calculate the due date for a book loan."""
        if not isinstance(loan_date, datetime):
            raise TypeError("Loan date must be a datetime object")

        if loan_days <= 0:
            raise ValueError("Loan days must be positive")

        return loan_date + timedelta(days=loan_days)

    def calculate_fine(self, days_overdue, book_type):
        """
        Calculate fine for overdue books.

        Fine rates:
        - Regular books: 0.50 PLN per day
        - Popular books: 1.00 PLN per day
        - Reference books: 2.00 PLN per day

        Maximum fine is 10x the daily rate.
        """
        if days_overdue <= 0:
            return 0.0

        if book_type not in self.LOAN_PERIODS:
            raise ValueError(f"Unknown book type: {book_type}")

        fine_rates = {
            self.REGULAR_BOOK: 0.5,
            self.POPULAR_BOOK: 1.0,
            self.REFERENCE_BOOK: 2.0
        }

        daily_rate = fine_rates[book_type]
        max_fine = daily_rate * 10

        fine = days_overdue * daily_rate
        return min(fine, max_fine)