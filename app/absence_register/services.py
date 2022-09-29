from datetime import date
from sys import stdout

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.fields.related_descriptors import ManyToManyDescriptor
from django.db.models.query import QuerySet
from django.db.utils import ProgrammingError

from absence_register.exceptions import InvalidAbsenceException
from core.models import (
    Absence,
    AbsenceDetail,
    ClassRoom,
    ClassroomAbsence,
    ClassroomStudent,
    StudentClassroom,
    TeacherClassroom,
    User,
)


class AbsenceFactory:
    STUDENT_GROUP = "student"
    _absences = Absence.objects

    def make_absence(self, **absence_data) -> Absence:
        """Creates and stores a absence

        Raises:
            InvalidAbsenceException: if invalid data is passed for creating the absence

        Returns:
            Absence: the new absence
        """
        absence_data.setdefault("absence_date", date.today())

        student: User | None = absence_data.get("student")

        if not student:
            raise InvalidAbsenceException("A student must be set")

        self._check_student(student)

        try:
            classroom: ClassRoom | None = absence_data.get("classroom")

        except ProgrammingError:
            stdout.write("Not able to load auth_group table")

        if not classroom:
            raise InvalidAbsenceException("A class room must be set")

        self._is_student_in_class(student, classroom)
        self._check_classroom_status(classroom)

        return self._absences.create(**absence_data)

    def _check_student(self, user_to_check: User) -> None:
        user_group: QuerySet[Group] = user_to_check.groups.filter(
            name=self.STUDENT_GROUP
        )

        if not user_group:
            raise InvalidAbsenceException("Invalid student")

    def _is_student_in_class(self, student: User, classroom: ClassRoom) -> None:
        class_members: ManyToManyDescriptor = classroom.members

        if student not in class_members.all():
            raise InvalidAbsenceException(f"Student {student} not in class {classroom}")

    def _check_classroom_status(self, classroom: ClassRoom) -> None:
        if not classroom.is_active:
            raise InvalidAbsenceException(f"Class {classroom} is not active anymore")


class ReadOnlyAbsenceFactory:
    _classroom_absences = ClassroomAbsence.objects
    _absence_details = AbsenceDetail.objects
    _student_classrooms = StudentClassroom.objects
    _classroom_students = ClassroomStudent.objects

    def __init__(self, absence: Absence) -> None:
        self._absence = absence

    def make_absence(self) -> ClassroomAbsence:
        """Saves the data for reading

        Returns:
            ClassroomAbsence: the read only absence data
        """
        absence_date: date = self._absence.absence_date
        classroom_absence = self._get_classroom_absence()

        absence_detail: AbsenceDetail = self._absence_details.create(
            absence_date=absence_date, classroom_absence=classroom_absence
        )
        absence_detail.save()

        absence_amount = self._get_absence_amount(classroom_absence)
        frequency = self._get_frequency(absence_amount)
        setattr(classroom_absence, "absence_amount", absence_amount)
        setattr(classroom_absence, "frequency", frequency)

        return classroom_absence

    def _get_classroom_absence(self) -> ClassroomAbsence:
        student_classroom = self._get_student_classroom()
        classroom_student = self._get_classroom_student()

        try:
            return self._classroom_absences.get(
                classroom__id=student_classroom.id,
                student__id=classroom_student.id,
            )

        except ObjectDoesNotExist:
            classroom_absence = self._classroom_absences.create(
                classroom=student_classroom,
                student=classroom_student,
            )
            classroom_absence.save()

            return classroom_absence

    def _get_student_classroom(self) -> StudentClassroom:
        user_id: int = self._absence.student.id
        classroom_id: int = self._absence.student.id

        try:
            return self._student_classrooms.get(
                user_id=user_id,
                classroom_id=classroom_id,
            )

        except ObjectDoesNotExist:
            student: str = self._absence.student.full_name

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
            student: str = self._absence.student.full_name

            classroom_student: ClassroomStudent = self._classroom_students.create(
                student=student, classroom=classroom
            )
            classroom_student.save()

            return classroom_student

    def _get_teacher_classroom(self) -> TeacherClassroom:
        classroom: ClassRoom = self._absence.classroom

        try:
            return TeacherClassroom.objects.get(classroom_id=classroom.id)

        except ObjectDoesNotExist:
            teacher_classroom = TeacherClassroom.objects.create(
                classroom_id=classroom.id, classroom=classroom.name
            )
            teacher_classroom.save()

            return teacher_classroom

    def _get_classroom_teachers(self) -> QuerySet[User]:
        classroom: ClassRoom = self._absence.classroom
        classroom_members: QuerySet[User] = get_user_model().objects.filter(
            classrooms__id=classroom.id
        )

        return classroom_members.filter(classrooms__members__groups__name="teacher")

    def _get_absence_amount(self, classroom_absence: ClassroomAbsence) -> int:
        absence_amount: int = classroom_absence.absence_amount

        return absence_amount + 1

    def _get_frequency(self, absence_amount: int) -> float:
        school_days: int = self._absence.classroom.school_days

        return (school_days - absence_amount) / school_days
