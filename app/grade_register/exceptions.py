from rest_framework.exceptions import ParseError


class InvalidGradeException(ParseError):
    """Raised when a grade is created with invalid data"""
