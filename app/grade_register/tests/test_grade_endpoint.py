from typing import Any

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Grade
from core.tests.helpers import make_fake_classroom, make_fake_student, make_fake_teacher

GRADE_REGISTER_URL = reverse("grades:grade-list")


class PrivateGradeEndpointTests(TestCase):
    """Tests for the private operations on grade end point"""

    def setUp(self) -> None:
        """Runs before each test"""
        teacher = make_fake_teacher()
        self._client = APIClient()
        self._client.force_authenticate(teacher)

    def test_create(self) -> None:
        """Test create grade"""
        arrangement = self._given_grade_data()
        result = self._when_post_request(arrangement)
        self._then_should_create_grade(result)

    def _given_grade_data(self) -> dict[str, object]:
        title = "Test 1"
        grade = 72
        student = make_fake_student()
        classroom = make_fake_classroom(student)

        return {
            "title": title,
            "grade": grade,
            "student": student.id,
            "classroom": classroom.id,
        }

    def _when_post_request(self, arrangement: dict[str, object]) -> Any:
        return self._client.post(GRADE_REGISTER_URL, arrangement)

    def _then_should_create_grade(self, result: Any) -> None:
        expected_status_code: int = status.HTTP_201_CREATED
        expected_result: Grade = Grade.objects.get(id=result.data.get("id"))

        self.assertEqual(expected_status_code, result.status_code)
        self.assertEqual(expected_result.grade, result.data.get("grade"))
