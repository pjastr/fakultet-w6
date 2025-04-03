class GradeCalculator:
    def calculate_grade(self, points, max_points):
        """
        Calculates a grade based on earned points.

        Args:
            points: number of earned points
            max_points: maximum possible points

        Returns:
            str: Grade in text form
        """
        if points < 0 or max_points <= 0:
            return "Invalid data"

        percentage = (points / max_points) * 100

        if percentage < 50:
            return "Fail"
        elif percentage < 60:
            return "Poor"
        elif percentage < 75:
            return "Satisfactory"
        elif percentage < 90:
            return "Good"
        else:
            return "Excellent"

    def has_passed(self, grade):
        """
        Checks if student has passed based on the grade.

        Args:
            grade: Grade in text form

        Returns:
            bool: True if passed, False otherwise
        """
        if grade == "Fail" or grade == "Invalid data":
            return False
        else:
            return True