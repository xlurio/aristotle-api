from datetime import date
from typing import Any
from django.test import TestCase
from rest_framework.test import APIClient
from app.core.tests.helpers import make_fake_student, make_fake_teacher
from core.tests.helpers import make_fake_classroom
from django.urls import reverse


absence_register_path = reverse("absence-list")


class PrivateAbsenceViewTests:
    """Tests for the absence end point private operations"""

    def setUp(self):
        """Will run before each test"""
        self._client = APIClient()

        teacher = make_fake_teacher(first_name="Teacher", password="12345")
        self._client.force_authenticate(teacher)

    def test_create(self) -> None:
        """Test registering a absence"""
        arrangement = self._given_request()
        result = self._when_requested(arrangement)
        self._then_should_register_absence(result)

    def _given_request(self) -> dict[str, object]:
        absence_date = date(year=2022, month=9, day=26)
        student = make_fake_student(first_name="Sample", password="12345")
        classroom = make_fake_classroom(student)

        return {
            "absence_date": absence_date,
            "classroom": [classroom.id],
            "student": [student.id],
        }

    def _when_requested(self, arrangement: dict[str, object]) -> Any:
        return self._client.post(absence_register_path, arrangement)

    def _then_should_register_absence(self, result: Any) -> None:
        pass
