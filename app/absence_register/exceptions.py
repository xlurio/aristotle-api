from rest_framework.exceptions import ParseError


class InvalidAbsenceException(ParseError):
    """Raised when a absence is created with invalid data"""
