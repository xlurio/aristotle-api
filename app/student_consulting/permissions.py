from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import View
from core.models import User


class IsStudent(BasePermission):
    """Views with this permission only allows students to access it"""

    def has_permission(self, request: Request, _: View):
        user: User = request.user
        student_permissions = ("view_grade", "view_absence")

        return user.has_perms(student_permissions)
