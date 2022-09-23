from django.contrib.auth.models import Group
from core.models import Absence, ClassRoom, User
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
