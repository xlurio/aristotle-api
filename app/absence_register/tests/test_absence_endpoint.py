from datetime import date
from typing import Any

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.tests.helpers import make_fake_classroom, make_fake_student, make_fake_teacher

ABSENCE_REGISTER_URL = reverse("absences:absence-list")


class PrivateAbsenceEndpointTests(TestCase):
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
        self._then_should_register_absence(arrangement, result)

    def _given_request(self) -> dict[str, object]:
        absence_date = date(year=2022, month=9, day=26)
        student = make_fake_student(first_name="Sample", password="12345")
        classroom = make_fake_classroom(student)

        return {
            "absence_date": absence_date,
            "classroom": classroom.id,
            "student": student.id,
        }

    def _when_requested(self, arrangement: dict[str, object]) -> Any:
        return self._client.post(ABSENCE_REGISTER_URL, arrangement)

    def _then_should_register_absence(
        self, arrangement: dict[str, object], result: Any
    ) -> None:
        expected_status_code = status.HTTP_201_CREATED
        actual_status_code = result.status_code

        expected_absence_date = str(arrangement.get("absence_date", ""))
        expected_classroom = arrangement.get("classroom", "")
        expected_student = arrangement.get("student", "")

        actual_absence_date = result.data.get("absence_date", "")
        actual_classroom = result.data.get("classroom", "")
        actual_student = result.data.get("student", "")

        self.assertEqual(expected_status_code, actual_status_code)
        self.assertEqual(expected_absence_date, actual_absence_date)
        self.assertEqual(expected_classroom, actual_classroom)
        self.assertEqual(expected_student, actual_student)
