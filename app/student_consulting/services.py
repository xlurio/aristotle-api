from datetime import date
from typing import Any
from core.models import User, Grade, ClassRoom, Absence
from django.db.models.query import QuerySet
from student_consulting.models import (
    GradeDetail,
    ReadOnlyAbsence,
    ReadOnlyGrade,
    Student,
)


class StudentDataFactory:
    """Factory for making student serialized data"""

    _grades = Grade.objects
    _abscenses = Absence.objects

    def __init__(self, student: User) -> None:
        self._student = student
        self._grade_instances: QuerySet[Grade] = self._grades.filter(
            student__id=self._student.id
        )
        self._absence_instances: QuerySet[Absence] = self._abscenses.filter(
            student__id=self._student.id
        )

    def make_data(self) -> dict[str, Any]:
        """serializes student data for reading

        Args:
            student (User): the current logged student

        Returns:
            dict[str, Any]: the serialized data
        """
        student_name = self._student.full_name
        grades = self._get_grades()
        absences = self._get_absences()

        return Student(student=student_name, grades=grades, absences=absences)

    def _get_grades(self) -> list[ReadOnlyGrade]:
        grade_classrooms: dict[int, ClassRoom] = self._get_grade_classrooms()

        classroom_id: int
        classroom_instance: ClassRoom
        classroom_name: str
        classroom_grade_instances: QuerySet[Grade] = []
        grade_details: list[GradeDetail] = []
        read_only_grade: ReadOnlyGrade
        grades: list[ReadOnlyGrade] = []
        average: float

        for classroom_id, classroom_instance in grade_classrooms.items():
            classroom_name = classroom_instance.name

            classroom_grade_instances = self._grade_instances.filter(
                classroom__id=classroom_id
            )
            grade_details = [
                GradeDetail(title=instance.title, grade=instance.grade)
                for instance in classroom_grade_instances
            ]

            average = self._get_grades_average(grade_details)

            read_only_grade = ReadOnlyGrade(
                classroom=classroom_name, average=average, grades=grade_details
            )

            grades.append(read_only_grade)

        return grades

    def _get_grade_classrooms(self) -> dict[int, ClassRoom]:
        grade_instance: Grade
        grade_classrooms: dict[int, ClassRoom] = {}

        for grade_instance in self._grade_instances:
            instance_classroom: ClassRoom = grade_instance.classroom
            grade_classrooms[instance_classroom.id] = instance_classroom

        return grade_classrooms

    def _get_grades_average(self, grade_instances: list[GradeDetail]) -> float:
        grade_instance: GradeDetail
        grade_sum: int = 0

        for grade_instance in grade_instances:
            grade_sum += grade_instance.grade

        number_of_grades = len(grade_instances)

        return grade_sum / number_of_grades

    def _get_absences(self) -> list[ReadOnlyAbsence]:
        absence_classrooms: dict[int, ClassRoom] = self._get_absence_classrooms()

        classroom_id: int
        classroom_instance: ClassRoom
        classroom_name: str
        classroom_absence_instances: QuerySet[Absence] = []
        absence_dates: list[date] = []
        read_only_absence: ReadOnlyAbsence
        absences: list[ReadOnlyAbsence] = []

        for classroom_id, classroom_instance in absence_classrooms.items():
            classroom_name = classroom_instance.name

            classroom_absence_instances = self._absence_instances.filter(
                classroom__id=classroom_id
            )

            absence_amount = classroom_absence_instances.count()

            frequency = absence_amount / classroom_instance.school_days

            absence_dates = [
                instance.absence_date for instance in classroom_absence_instances
            ]

            read_only_absence = ReadOnlyAbsence(
                classroom=classroom_name,
                absence_amount=absence_amount,
                frequency=frequency,
                absence_dates=absence_dates,
            )

            absences.append(read_only_absence)

        return absences

    def _get_absence_classrooms(self) -> dict[int, ClassRoom]:
        absence_instance: Absence
        absence_classrooms: dict[int, ClassRoom] = {}

        for absence_instance in self._absence_instances:
            instance_classroom: ClassRoom = absence_instance.classroom
            absence_classrooms[instance_classroom.id] = instance_classroom

        return absence_classrooms
