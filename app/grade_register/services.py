from sys import stdout
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import ProgrammingError
from core.models import (
    ClassRoom,
    ClassroomGrade,
    ClassroomStudent,
    Grade,
    GradeDetail,
    StudentClassroom,
    TeacherClassroom,
    User,
)
from grade_register.exceptions import InvalidGradeException


class GradeFactory:
    """Factory for creating new grade objects"""

    STUDENT_GROUP = "student"
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

        try:
            self._check_student(student)
        except ProgrammingError:
            stdout.write("Not able to load auth_group table")

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
            raise InvalidGradeException("A title must be set")

    def _check_grade(self, grade: int) -> None:
        is_positive: bool = grade >= 0
        is_lower_or_equal_to_10 = grade <= 100
        is_grade_valid = is_positive and is_lower_or_equal_to_10

        if not is_grade_valid:
            raise InvalidGradeException("Grades must be between 0 and 100")

    def _check_student(self, user_to_check: User) -> None:
        user_groups = user_to_check.groups.filter(name=self.STUDENT_GROUP)

        if not user_groups:
            raise InvalidGradeException("Invalid student")

    def _is_student_in_class(self, student: User, classroom: ClassRoom) -> None:
        class_members = classroom.members.filter(id=student.id)

        if not class_members:
            raise InvalidGradeException(f"Student {student} not in class {classroom}")

    def _check_classroom_status(self, classroom: ClassRoom) -> None:
        if not classroom.is_active:
            raise InvalidGradeException(f"Class {classroom} is not active anymore")


class ReadOnlyGradeFactory:
    """Factory for creating read only grades"""

    _student_classrooms = StudentClassroom.objects
    _classroom_students = ClassroomStudent.objects
    _classroom_grades = ClassroomGrade.objects
    _grade_details = GradeDetail.objects

    def __init__(self, grade: Grade) -> None:
        self._grade = grade

    def make_grade(self) -> ClassroomGrade:
        title: str = self._grade.title
        grade_value: int = self._grade.grade
        classroom_grade = self._get_classroom_grade()

        grade_details: GradeDetail = self._grade_details.create(
            title=title, grade_value=grade_value, classroom_grade=classroom_grade
        )
        grade_details.save()

        average = self._get_average(classroom_grade)
        setattr(classroom_grade, "average", average)

        return classroom_grade

    def _get_classroom_grade(self) -> ClassroomGrade:
        student_classroom = self._get_student_classroom()
        classroom_student = self._get_classroom_student()

        try:
            return self._classroom_grades.get(
                classroom__id=student_classroom.id,
                student__id=classroom_student.id,
            )

        except ObjectDoesNotExist:
            classroom_grade: ClassroomGrade = self._classroom_grades.create(
                classroom=student_classroom,
                student=classroom_student,
            )
            classroom_grade.save()

            return classroom_grade

    def _get_student_classroom(self) -> StudentClassroom:
        user_id: int = self._grade.student.id
        classroom_id: int = self._grade.student.id

        try:
            return self._student_classrooms.get(
                user_id=user_id,
                classroom_id=classroom_id,
            )

        except ObjectDoesNotExist:
            student: str = self._grade.student.full_name

            student_classroom: StudentClassroom = self._student_classrooms.create(
                user_id=user_id,
                student=student,
                classroom_id=classroom_id,
            )
            student_classroom.save()

            return student_classroom

    def _get_classroom_student(self) -> ClassroomStudent:
        classroom: TeacherClassroom = self._get_teacher_classroom()

        try:
            return self._classroom_students.get(classroom__id=classroom.id)

        except ObjectDoesNotExist:
            student: str = self._grade.student.full_name

            classroom_student: ClassroomStudent = self._classroom_students.create(
                student=student, classroom=classroom
            )
            classroom_student.save()

            return classroom_student

    def _get_teacher_classroom(self) -> TeacherClassroom:
        classroom: ClassRoom = self._grade.classroom

        try:
            return TeacherClassroom.objects.get(classroom_id=classroom.id)

        except ObjectDoesNotExist:
            teacher_classroom = TeacherClassroom.objects.create(
                classroom_id=classroom.id, classroom=classroom.name
            )
            teacher_classroom.save()

            return teacher_classroom

    def _get_average(self, grade: ClassroomGrade) -> float:
        grades: list[int] = grade.grade_values.all()
        grades_sum: int = 0

        for grade_detail in grades:
            grades_sum += grade_detail.grade_value

        number_of_grades = len(grades)

        return grades_sum / number_of_grades
