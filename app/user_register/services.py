from typing import Any, Callable, Dict
import uuid
from core.models import Absence, Grade, User
from core.exceptions import InvalidUserException
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

    def make_professor_group(self) -> Group:
        professor_group, _ = Group.objects.get_or_create(name="professor")

        models = [Absence, Grade]
        content_types = [ContentType.objects.get_for_model(model) for model in models]
        professor_permissions = Permission.objects.filter(
            content_type__in=content_types
        )

        for permission in professor_permissions:
            if permission not in professor_group.permissions:
                professor_group.add(permission)

        return professor_group

    def make_student_group(self) -> Group:
        student_group, _ = Group.objects.get_or_create(name="student")

        models = [Absence, Grade]
        content_types = [ContentType.objects.get_for_model(model) for model in models]
        student_permissions = Permission.objects.filter(
            content_type__in=content_types, codename__startswith="view_"
        )

        for permission in student_permissions:
            if permission not in student_group.permissions:
                student_group.add(permission)

        return student_group


class UserFactory:
    """Service for creating users"""

    _users = get_user_model().objects
    _groups = GroupFactory()

    def make_user(self, **user_data: Dict[str, Any]) -> User:
        """Creates and stores an user object

        Args:
            user_data (Dict[str, Any]): data needed for creating new users

        Raises:
            InvalidUserException: raised when invalid data was passed for creating the
            user

        Returns:
            User: the user created
        """

        user_data["register"] = generate_register()

        first_name = user_data.get("first_name", "")
        last_name = user_data.get("last_name", "")

        first_name = self._validate_name(first_name)
        last_name = self._validate_name(last_name)

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
            "student": self._make_professor,
            "teacher": self._make_professor,
            "staff": self._make_superuser,
        }

        return creation_method_dict.get(role)

    def _make_professor(self, password: str, **kwargs: Any) -> User:
        professor_group = self._groups.make_professor_group()

        professor = self._users.create_user(password, **kwargs)
        professor.groups.add(professor_group)

        professor.save()

        return professor

    def _make_professor(self, password: str, **kwargs) -> User:
        student_group = self._groups.make_student_group()

        student = self._users.create_user(password, **kwargs)
        student.groups.add(student_group)

        student.save()

        return student

    def _make_superuser(self, password: str, **kwargs) -> User:
        return self._users.create_superuser(password, **kwargs)
