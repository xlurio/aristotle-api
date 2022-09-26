from datetime import date
from django.test import TestCase
from absence_register.services import AbsenceFactory
from core.tests.helpers import make_fake_classroom, make_fake_student
from core.adapters import UserManager
from core.models import Absence, ClassRoom
from django.contrib.auth import get_user_model


class AbsenceFactoryTests(TestCase):
    """Test absence factory"""

    _students: UserManager = get_user_model().objects
    _classrooms = ClassRoom.objects

    def test_make_absence(self) -> None:
        """Test creating absence object"""
        arrangement = self._given_absence_data()
        result = self._when_absence_made(arrangement)
        self._then_should_create_absence(result)

    def _given_absence_data(self) -> dict[str, object]:
        absence_date = date(year=2022, month=9, day=25)

        student = make_fake_student(
            first_name="Sample", last_name="Student", password="12345"
        )

        classroom = make_fake_classroom(student)

        return {
            "absence_date": absence_date,
            "student": student,
            "classroom": classroom,
        }

    def _when_absence_made(self, arrangement: dict[str, object]) -> Absence:
        factory = AbsenceFactory()
        new_absence = factory.make_absence(**arrangement)
        new_absence.save()

        return new_absence

    def _then_should_create_absence(self, result: Absence) -> None:
        expected_result = Absence.objects.get(id=result.id)

        self.assertTrue(isinstance(result, Absence))
        self.assertEqual(expected_result.id, result.id)
