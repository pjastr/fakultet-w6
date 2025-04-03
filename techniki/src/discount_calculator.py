class DiscountCalculator:
    """
    Calculates discount based on purchase amount.

    Discount rules:
    - 0% discount for purchases under 100 PLN
    - A 5% discount for purchases between 100 and 499.99 PLN
    - A 10% discount for purchases between 500 and 999.99 PLN
    - A 15% discount for purchases of 1000 PLN or more

    Additionally, when calculating final price after discount:
    - If customer has loyalty card, add extra 2% discount
    - If purchase includes at least 5 different items, add extra 1% discount
    - If purchase is made on weekend (Saturday or Sunday), add extra 1% discount
    """

    def calculate_discount_percentage(self, amount):
        """Calculate base discount percentage based on purchase amount."""
        if amount < 0:
            raise ValueError("Purchase amount cannot be negative")

        if amount < 100:
            return 0
        elif amount < 500:
            return 5
        elif amount < 1000:
            return 10
        else:
            return 15

    def calculate_final_price(self, amount, has_loyalty_card=False,
                              different_items_count=1, is_weekend=False):
        """Calculate final price after all applicable discounts."""
        if amount < 0:
            raise ValueError("Purchase amount cannot be negative")
        if different_items_count < 1:
            raise ValueError("Number of different items must be at least 1")

        # Base discount based on amount
        discount_percentage = self.calculate_discount_percentage(amount)

        # Additional discounts
        if has_loyalty_card:
            discount_percentage += 2

        if different_items_count >= 5:
            discount_percentage += 1

        if is_weekend:
            discount_percentage += 1

        # Calculate final price
        discount_amount = amount * (discount_percentage / 100)
        return round(amount - discount_amount, 2)