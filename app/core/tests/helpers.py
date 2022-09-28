import uuid
from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from core.models import (
    Absence,
    AbsenceDetail,
    ClassRoom,
    ClassroomAbsence,
    ClassroomGrade,
    ClassroomStudent,
    Grade,
    GradeDetail,
    StudentClassroom,
    TeacherClassroom,
    User,
)


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
        if permission not in teacher_group.permissions.all():
            teacher_group.permissions.add(permission)

    return teacher_group


def make_fake_student(password: str = "12345", **kwargs: object) -> User:
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


def make_fake_teacher(password: str = "12345", **kwargs: object) -> User:
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


def make_fake_staff(password: str = "12345", **kwargs: object) -> User:
    """Create staff user for tests"""
    kwargs.setdefault("register", "light-123")
    return get_user_model().objects.create_superuser(password, **kwargs)


def make_fake_classroom(member: User, subject="mathematics") -> ClassRoom:
    """Creates a classroom object for tests

    Args:
        member (User): first member of the class room
        subject (str, optional): class subject. Defaults to "mathematics".

    Returns:
        ClassRoom: the created class room
    """
    name = f"{subject}-123"
    start = date(year=2022, month=8, day=10)
    deadline = date(year=2022, month=12, day=10)

    classroom: ClassRoom = ClassRoom.objects.create(
        subject=subject, name=name, start=start, deadline=deadline
    )
    classroom.members.add(member)
    classroom.save()

    return classroom


def make_fake_grade(
    student: User, classroom: ClassRoom, title: str = "Test 1", grade=90
) -> Grade:
    """Creates a grade object for tests

    Args:
        student (User): student to receive the grade
        classroom (ClassRoom): the class room of the grade
        title (str, optional): the origin of the grade. Defaults to "Test 1".
        grade (int, optional): the grade value. Defaults to 90.

    Returns:
        Grade: the created grade object
    """
    new_grade: Grade = Grade.objects.create(
        student=student, classroom=classroom, title=title, grade=grade
    )
    new_grade.save()

    return new_grade


def make_fake_absence(
    student: User,
    classroom: ClassRoom,
    absence_date: date = date(year=2022, month=9, day=27),
) -> Absence:
    """Creates a absence object for tests

    Args:
        student (User): student to receive the absence
        classroom (ClassRoom): the class of the absence
        absence_date (date, optional): the date of the absence. Defaults to
        date(year=2022, month=9, day=27).

    Returns:
        Absence: the new absence object
    """
    new_absence: Absence = Absence.objects.create(
        student=student,
        classroom=classroom,
        absence_date=absence_date,
    )
    new_absence.save()

    return new_absence


def make_fake_student_classroom(
    student: User, classroom: ClassRoom
) -> StudentClassroom:
    """Create a student class room object for tests

    Args:
        student (User): the student
        classroom (ClassRoom): the class room of the student

    Returns:
        StudentClassroom: the new student class room data for reading
    """
    new_classroom = StudentClassroom.objects.create(
        user_id=student.id,
        classroom_id=classroom.id,
        student=student.full_name,
    )
    new_classroom.save()

    return new_classroom


def make_fake_teacher_classroom(classroom: ClassRoom) -> TeacherClassroom:
    """Create a teacher class room object for tests

    Args:
        classroom (ClassRoom): the teacher class room

    Returns:
        TeacherClassroom: the teacher class room data for reading
    """
    new_classroom = TeacherClassroom.objects.create(
        classroom_id=classroom.id, classroom=classroom.name
    )
    new_classroom.save()

    return new_classroom


def make_fake_classroom_student(
    student: User, teacher_classroom: TeacherClassroom
) -> ClassroomStudent:
    """Create a class room student object for tests

    Args:
        student (User): the class room student
        teacher_classroom (TeacherClassroom): the teacher class room

    Returns:
        ClassroomStudent: the student data for reading
    """
    new_student = ClassroomStudent.objects.create(
        student=student.full_name, classroom=teacher_classroom
    )
    new_student.save()

    return new_student


def make_fake_classroom_grade(
    student_classroom: StudentClassroom, classroom_student: ClassroomStudent
) -> ClassroomGrade:
    """Create a class room grade object for tests

    Args:
        student_classroom (StudentClassroom): the class room
        classroom_student (ClassroomStudent): the student

    Returns:
        ClassroomGrade: the grade data for reading
    """
    new_grade = ClassroomGrade.objects.create(
        classroom=student_classroom, student=classroom_student
    )
    new_grade.save()

    return new_grade


def make_fake_grade_detail(
    grade: Grade, classroom_grade: ClassroomGrade
) -> GradeDetail:
    """Create a grade detail object for tests

    Args:
        grade (Grade): the related grade data
        classroom_grade (ClassroomGrade): the related class room grade object

    Returns:
        GradeDetail: the grade detailed data for reading
    """
    new_detail = GradeDetail.objects.create(
        title=grade.title, grade_value=grade.grade, classroom_grade=classroom_grade
    )
    new_detail.save()

    return new_detail


def make_fake_classroom_absence(
    student_classroom: StudentClassroom, classroom_student: ClassroomStudent
) -> ClassroomAbsence:
    """Create class room absence object for tests

    Args:
        student_classroom (StudentClassroom): the class room data
        classroom_student (ClassroomStudent): the student data

    Returns:
        ClassroomAbsence: the absence data for further reading
    """
    new_absence = ClassroomAbsence.objects.create(
        classroom=student_classroom, student=classroom_student
    )
    new_absence.save()

    return new_absence


def make_fake_absence_detail(
    absence: Absence, classroom_absence: ClassroomAbsence
) -> AbsenceDetail:
    """Create absence detail object for tests

    Args:
        absence (Absence): the related absence object
        classroom_absence (ClassroomAbsence): the related class room absence object

    Returns:
        AbsenceDetail: the absence detailed data for reading
    """
    new_detail = AbsenceDetail.objects.create(
        absence_date=absence.absence_date, classroom_absence=classroom_absence
    )
    new_detail.save()

    return new_detail
