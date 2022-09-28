from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import View

from core.models import Absence, Grade, User


class IsTeacher(BasePermission):
    """Views with this permission only allows students to access it"""

    def has_permission(self, request: Request, _: View):
        models = [Absence, Grade]
        content_types: list[ContentType] = [
            ContentType.objects.get_for_model(model) for model in models
        ]
        teacher_permissions: QuerySet[Permission] = Permission.objects.filter(
            content_type__in=content_types
        )
        teacher_permissions_codenames = [
            f"core.{permission.codename}" for permission in teacher_permissions
        ]

        user: User = request.user

        return user.has_perms(teacher_permissions_codenames)
