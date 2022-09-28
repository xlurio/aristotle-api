from django.test import TestCase

from core.models import Grade
from core.tests.helpers import make_fake_classroom, make_fake_student
from grade_register.services import GradeFactory


class GradeFactoryTests(TestCase):
    """Tests for the grade factory"""

    def test_make_grade(self) -> None:
        """Test making grade"""
        arrangement = self._given_grade_data()
        result = self._when_grade_made(arrangement)
        self._then_should_create_grade(result)

    def _given_grade_data(self) -> dict[str, object]:
        title = "Test 1"
        grade = 82
        student = make_fake_student(password="12345")
        classroom = make_fake_classroom(student)

        return {
            "title": title,
            "grade": grade,
            "student": student,
            "classroom": classroom,
        }

    def _when_grade_made(self, arrangement: dict[str, object]) -> Grade:
        factory = GradeFactory()

        return factory.make_grade(**arrangement)

    def _then_should_create_grade(self, result: Grade) -> None:
        expected_result = Grade.objects.get(id=result.id)

        self.assertEqual(expected_result.grade, result.grade)
