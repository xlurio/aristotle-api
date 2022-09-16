from datetime import date
from core.models import ClassRoom, Grade, User
from django.contrib.auth.models import Group
from core.exceptions import InvalidGradeException


class GradeFactory:
    STUDENT_GROUP, _ = Group.objects.get_or_create(name="student")
    _grades = Grade.objects

    def make_grade(self, **grade_data) -> Grade:
        """Creates and stores a grade

        Raises:
            InvalidGradeException: if invalid data is passed for creating the grade

        Returns:
            Grade: the new grade
        """
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
        today = date.today()
        did_class_begun = today > classroom.start
        did_class_ended = today > classroom.deadline
        is_date_valid = did_class_begun and not did_class_ended

        if not is_date_valid:
            raise InvalidGradeException(f"Class {classroom} is not active anymore")
