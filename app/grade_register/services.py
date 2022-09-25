from datetime import date
from core.models import ClassRoom, Grade, ReadOnlyGrade, Student, User
from django.contrib.auth.models import Group
from django.db.models.query import QuerySet
from django.core.exceptions import ObjectDoesNotExist
from grade_register.exceptions import InvalidGradeException


class GradeFactory:
    """Factory for creating new grade objects"""

    STUDENT_GROUP, _ = Group.objects.get_or_create(name="student")
    _grades = Grade.objects

    def make_grade(self, **grade_data) -> Grade:
        """Creates and stores a grade

        Raises:
            InvalidGradeException: if invalid data is passed for creating the grade

        Returns:
            Grade: the new grade
        """
        title: str = grade_data.get("title", "")
        self._check_title(title)

        grade: int = grade_data.get("grade", 0)
        self._check_grade(grade)

        student = grade_data.get("student")

        if not student:
            raise InvalidGradeException("A student must be set")

        self._check_student(student)

        classroom = grade_data.get("classroom")

        if not classroom:
            raise InvalidGradeException("A class room must be set")

        self._is_student_in_class(student, classroom)
        self._check_classroom_status(classroom)

        return self._grades.create(**grade_data)

    def _check_title(self, title: str) -> None:
        title_length = len(title)
        is_title_empty = title_length < 1

        if is_title_empty:
            raise InvalidGradeException(f"A title must be set")

    def _check_grade(self, grade: int) -> None:
        is_positive = grade >= 0
        is_lower_or_equal_to_10 = grade <= 100
        is_grade_valid = is_positive and is_lower_or_equal_to_10

        if not is_grade_valid:
            raise InvalidGradeException("Grades must be between 0 and 100")

    def _check_student(self, user_to_check: User) -> None:
        user_groups = user_to_check.groups

        if self.STUDENT_GROUP not in user_groups:
            raise InvalidGradeException("Invalid student")

    def _is_student_in_class(self, student: User, classroom: ClassRoom) -> None:
        class_members = classroom.members

        if student not in class_members:
            raise InvalidGradeException(f"Student {student} not in class {classroom}")

    def _check_classroom_status(self, classroom: ClassRoom) -> None:
        if not classroom.is_active:
            raise InvalidGradeException(f"Class {classroom} is not active anymore")


class ReadOnlyGradeFactory:
    """Factory for creating read only grades"""

    _students = Student.objects
    _read_only_grades = ReadOnlyGrade.objects
    _grades = Grade.objects

    def __init__(self, grade: Grade) -> None:
        self._grade = grade

    def make_grade(self) -> ReadOnlyGrade:
        classroom: str = self._grade.classroom.name
        average = self._get_average()
        student, _ = self._get_student()

        return self._read_only_grades.create(
            classroom=classroom, average=average, student=student
        )

    def _get_average(self) -> float:
        student_grades: QuerySet[Grade] = self._grades.filter(
            student__id=self._grade.student.id,
        )
        classroom_grades: QuerySet[Grade] = student_grades.filter(
            classroom__id=self._grade.classroom.id,
        )
        grade_instance: Grade
        grade_sum: int

        for grade_instance in classroom_grades:
            grade_sum += grade_instance.grade

        number_of_grades = len(classroom_grades)

        return grade_sum / number_of_grades

    def _get_student(self) -> Student:
        try:
            student = self._students.get(user_id=self._grade.student.id)
            return student

        except ObjectDoesNotExist:
            student_user: User = self._grade.student
            student = self._students.create(
                user_id=student_user.id, student=student_user.full_name
            )
            student.save()

            return student
