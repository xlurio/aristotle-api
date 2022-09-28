from datetime import date

from django.test import TestCase

from absence_register.services import ReadOnlyAbsenceFactory
from core.models import Absence, ClassroomAbsence
from core.tests.helpers import make_fake_classroom, make_fake_student


class ReadOnlyAbsenceFactoryTests(TestCase):
    """Tests for the read only absence factory"""

    def test_make_absence(self) -> None:
        """Test making absence object"""
        arrangement = self._given_absence_object()
        result = self._when_make_absence(arrangement)
        self._then_should_create_classroom_absence(result)

    def _given_absence_object(self) -> Absence:
        absence_date = date(year=2022, month=9, day=27)
        student = make_fake_student(
            first_name="John", last_name="Travolta", password="12345"
        )
        classroom = make_fake_classroom(student)

        return Absence.objects.create(
            absence_date=absence_date, classroom=classroom, student=student
        )

    def _when_make_absence(self, arrangement: Absence) -> ClassroomAbsence:
        factory = ReadOnlyAbsenceFactory(arrangement)

        return factory.make_absence()

    def _then_should_create_classroom_absence(self, result: ClassroomAbsence) -> None:
        expected_result = ClassroomAbsence.objects.get(id=result.id)

        expected_student = "John Travolta"
        actual_student = result.student.student

        self.assertEqual(expected_result.id, result.id)
        self.assertEqual(expected_student, actual_student)
