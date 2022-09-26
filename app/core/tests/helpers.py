from datetime import date
from typing import Any, Callable
import uuid
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from core.models import Absence, ClassRoom, Grade, User
from django.contrib.contenttypes.models import ContentType


def generate_fake_register() -> str:
    """Generates a registration number for tests

    Returns:
        str: the registration number
    """
    registry = uuid.uuid4()

    return str(registry)


def _make_fake_student_group() -> Group:
    """Create or get the students group for tests

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
        if permission not in student_group.permissions.all():
            student_group.permissions.add(permission)

    return student_group


def _make_fake_teacher_group() -> Group:
    """Create or get the teachers group for tests

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


def make_fake_student(password: str, **kwargs: object) -> User:
    """Creates a student for testing

    Args:
        password (str): student password

    Returns:
        User: student created
    """
    student_group = _make_fake_student_group()

    first_name: str = kwargs.get("first_name", "")
    kwargs["register"] = f"{first_name.lower()}-{generate_fake_register()}"

    student: User = get_user_model().objects.create_user(password=password, **kwargs)
    student.groups.add(student_group)

    student.save()

    return student


def make_fake_teacher(password: str, **kwargs: object) -> User:
    """Creates a student for testing

    Args:
        password (str): student password

    Returns:
        User: student created
    """
    teacher_group = _make_fake_teacher_group()

    first_name: str = kwargs.get("first_name", "")
    kwargs["register"] = f"{first_name.lower()}-{generate_fake_register()}"

    teacher: User = get_user_model().objects.create_user(password=password, **kwargs)
    teacher.groups.add(teacher_group)

    teacher.save()

    return teacher


def make_fake_classroom(member: User) -> ClassRoom:
    """Creates a classroom object for tests"""
    subject = "mathematics"
    name = "mathematics-123"
    start = date(year=2022, month=8, day=10)
    deadline = date(year=2022, month=12, day=10)

    classroom: ClassRoom = ClassRoom.objects.create(
        subject=subject, name=name, start=start, deadline=deadline
    )
    classroom.members.add(member)
    classroom.save()

    return classroom
