from datetime import date
from typing import Any

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import ClassRoom
from core.tests.helpers import make_fake_staff

CLASSROOM_CREATION_URL = reverse("classrooms:classroom-list")


class PrivateClassroomEndpointTests(TestCase):
    """Tests the private operations on the class room registering end point"""

    def setUp(self) -> None:
        """Runs before each test"""
        staff = make_fake_staff()

        self._client = APIClient()
        self._client.force_authenticate(staff)

    def test_create(self) -> None:
        """Test create classroom"""
        arrangement = self._given_classroom_data()
        result = self._when_post_request(arrangement)
        self._then_should_create_classroom(result)

    def _given_classroom_data(self) -> dict[str, object]:
        subject = "mathematics"
        start = date(year=2022, month=8, day=10)
        deadline = date(year=2022, month=12, day=10)

        return {"subject": subject, "start": start, "deadline": deadline}

    def _when_post_request(self, arrangement: dict[str, object]) -> Any:
        return self._client.post(CLASSROOM_CREATION_URL, arrangement)

    def _then_should_create_classroom(self, result: Any) -> None:
        expected_status_code = status.HTTP_201_CREATED
        actual_status_code = result.status_code

        result_id: str = result.data.get("id", -1)
        result_id = int(result_id)
        expected_classroom: ClassRoom = ClassRoom.objects.get(id=result_id)

        self.assertEqual(expected_status_code, actual_status_code)
        self.assertEqual(expected_classroom.subject, result.data.get("subject"))
