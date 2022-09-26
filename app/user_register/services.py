from typing import Any, Callable
import uuid
from core.models import Absence, Grade, User
from user_register.exceptions import InvalidUserException
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


def generate_register() -> str:
    """Generates a registration number

    Returns:
        str: the registration number
    """
    registry = uuid.uuid4()

    return str(registry)


class GroupFactory:
    """Service for creating group objects"""

    def make_teacher_group(self) -> Group:
        """Create or get the teachers group

        Returns:
            Group: the teachers group
        """
        teacher_group, _ = Group.objects.get_or_create(name="teacher")

        models = [Absence, Grade]
        content_types = [ContentType.objects.get_for_model(model) for model in models]
        teacher_permissions = Permission.objects.filter(content_type__in=content_types)

        for permission in teacher_permissions:
            if permission not in teacher_group.permissions:
                teacher_group.permissions.add(permission)

        return teacher_group

    def make_student_group(self) -> Group:
        """Create or get the students group

        Returns:
            Group: the students group
        """
        student_group, _ = Group.objects.get_or_create(name="student")

        models = [Absence, Grade]
        content_types = [ContentType.objects.get_for_model(model) for model in models]
        student_permissions = Permission.objects.filter(
            content_type__in=content_types, codename__startswith="view_"
        )

        for permission in student_permissions:
            if permission not in student_group.permissions:
                student_group.permissions.add(permission)

        return student_group


class UserFactory:
    """Service for creating users"""

    _users = get_user_model().objects
    _groups = GroupFactory()

    def make_user(self, **user_data: Any) -> User:
        """Creates and stores an user object

        Args:
            user_data (Dict[str, Any]): data needed for creating new users

        Raises:
            InvalidUserException: raised when invalid data was passed for creating the
            user

        Returns:
            User: the user created
        """

        first_name = user_data.get("first_name", "")
        last_name = user_data.get("last_name", "")

        first_name = self._validate_name(first_name)
        last_name = self._validate_name(last_name)

        user_data["register"] = f"{first_name.lower()}-{generate_register()}"

        role = user_data.pop("role")
        creation_method = self._get_creation_method(role)

        if creation_method:
            return creation_method(
                **user_data,
            )

        raise InvalidUserException(f"{role} is not a valid role")

    def _validate_name(self, name: str) -> str:
        if not name:
            raise InvalidUserException("The full name must be set")

        return name.capitalize()

    def _get_creation_method(self, role: str) -> Callable[[Any], User]:
        creation_method_dict = {
            "student": self._make_student,
            "teacher": self._make_teacher,
            "staff": self._make_superuser,
        }
        creation_method = creation_method_dict.get(role)

        if creation_method:
            return creation_method

        raise InvalidUserException(f"{role} is not a valid role")

    def _make_teacher(self, password: str, **kwargs: Any) -> User:
        teacher_group = self._groups.make_teacher_group()

        teacher = self._users.create_user(password, **kwargs)
        teacher.groups.add(teacher_group)

        teacher.save()

        return teacher

    def _make_student(self, password: str, **kwargs: Any) -> User:
        student_group = self._groups.make_student_group()

        student = self._users.create_user(password, **kwargs)
        student.groups.add(student_group)

        student.save()

        return student

    def _make_superuser(self, password: str, **kwargs: Any) -> User:
        return self._users.create_superuser(password=password, **kwargs)
