from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import View
from core.models import Absence, Grade, User
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission


class IsTeacher(BasePermission):
    """Views with this permission only allows students to access it"""

    def has_permission(self, request: Request, _: View):
        models = [Absence, Grade]
        content_types = [ContentType.objects.get_for_model(model) for model in models]
        teacher_permissions = Permission.objects.filter(content_type__in=content_types)

        user: User = request.user

        return user.has_perms(teacher_permissions)
