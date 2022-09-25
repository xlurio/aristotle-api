from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query import QuerySet
from core.models import Absence, ClassRoom, ReadOnlyAbsence, Student, User
from absence_register.exceptions import InvalidAbsenceException
from datetime import date


class AbsenceFactory:
    STUDENT_GROUP = Group.objects.get(name="student")
    _absences = Absence.objects

    def make_absence(self, **absence_data) -> Absence:
        """Creates and stores a absence

        Raises:
            InvalidAbsenceException: if invalid data is passed for creating the absence

        Returns:
            Absence: the new absence
        """
        absence_data.setdefault("absence_date", date.today())

        student = absence_data.get("student")

        if not student:
            raise InvalidAbsenceException("A student must be set")

        self._check_student(student)

        classroom = absence_data.get("classroom")

        if not classroom:
            raise InvalidAbsenceException("A class room must be set")

        self._is_student_in_class(student, classroom)
        self._check_classroom_status(classroom)

        return self._absences.create(**absence_data)

    def _check_student(self, user_to_check: User) -> None:
        user_groups = user_to_check.groups

        if self.STUDENT_GROUP not in user_groups:
            raise InvalidAbsenceException("Invalid student")

    def _is_student_in_class(self, student: User, classroom: ClassRoom) -> None:
        class_members = classroom.members

        if student not in class_members:
            raise InvalidAbsenceException(f"Student {student} not in class {classroom}")

    def _check_classroom_status(self, classroom: ClassRoom) -> None:
        if not classroom.is_active:
            raise InvalidAbsenceException(f"Class {classroom} is not active anymore")


class ReadOnlyAbsenceFactory:
    _absences = Absence.objects
    _read_only_absences = ReadOnlyAbsence.objects
    _students = Student.objects

    def __init__(self, absence: Absence) -> None:
        self._absence = absence
        self._student_absences = self._get_student_absences()

    def _get_student_absences(self) -> QuerySet[Absence]:
        student_user: User = self._absence.student
        student_absences: QuerySet[Absence] = self._absences.filter(
            student__id=student_user
        )

        classroom: ClassRoom = self._absence.classroom

        return student_absences.filter(classroom__id=classroom.id)

    def make_absence(self) -> ReadOnlyAbsence:
        classroom: str = self._absence.classroom.name
        absence_amount = len(self._student_absences)
        frequency = self._get_frequency()
        student, _ = self._get_student()

        return self._read_only_absences.create(
            classroom=classroom,
            absence_amount=absence_amount,
            frequency=frequency,
            student=student,
        )

    def _get_frequency(self) -> float:
        classroom: ClassRoom = self._absence.classroom
        school_days = classroom.school_days
        number_of_absences = len(self._student_absences)

        return (school_days - number_of_absences) / school_days

    def _get_student(self) -> Student:
        try:
            student: Student = self._students.get(user_id=self._absence.student.id)
            return student

        except ObjectDoesNotExist:
            student_user: User = self._absence.student
            student: Student = self._students.create(
                user_id=student_user.id, student=student_user.full_name
            )
            student.save()

            return student
