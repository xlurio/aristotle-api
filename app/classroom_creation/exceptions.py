from rest_framework.exceptions import ParseError


class InvalidClassRoomException(ParseError):
    """Raised when a class room is created with invalid data"""
