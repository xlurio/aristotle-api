from rest_framework.permissions import BasePermission


class IsProfessor(BasePermission):
    """Allow access to professors"""
