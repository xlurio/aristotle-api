from datetime import date

from django.test import TestCase

from classroom_creation.services import ClassRoomFactory
from core.models import ClassRoom


class ClassroomFactoryTests(TestCase):
    """Tests for the class room factory"""

    def test_make_classroom(self) -> None:
        """Test creating a class room"""
        arrangement = self._given_classroom_data()
        result = self._when_classroom_made(arrangement)
        self._then_should_create_classroom(result)

    def _given_classroom_data(self) -> dict[str, object]:
        subject = "mathematics"
        start = date(year=2022, month=8, day=10)
        deadline = date(year=2022, month=12, day=10)

        return {"subject": subject, "start": start, "deadline": deadline}

    def _when_classroom_made(self, arrangement: dict[str, object]) -> ClassRoom:
        factory = ClassRoomFactory()

        return factory.make_classroom(**arrangement)

    def _then_should_create_classroom(self, result: ClassRoom) -> None:
        expected_result: ClassRoom = ClassRoom.objects.get(id=result.id)

        self.assertEqual(expected_result.deadline, result.deadline)
