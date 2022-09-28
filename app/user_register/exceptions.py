from rest_framework.exceptions import ParseError


class InvalidUserException(ParseError):
    """Raised when an user is created with invalid data"""
