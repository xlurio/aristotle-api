from typing import Any

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.tests import helpers

USER_REGISTER_URL = reverse("users:user-list")


class PrivateUserEndpointTests(TestCase):
    """Tests for private operations on user end point"""

    def setUp(self) -> None:
        """Runs before each test"""
        staff = helpers.make_fake_staff()

        self._client = APIClient()
        self._client.force_authenticate(staff)

    def test_create(self) -> None:
        """Test creating user"""
        arrangement = self._given_user_data()
        result = self._when_post_request(arrangement)
        self._then_should_create_user(result)

    def _given_user_data(self) -> dict[str, object]:
        first_name = "Tom"
        last_name = "Cruise"
        password = "12345"
        role = "student"

        return {
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
            "role": role,
        }

    def _when_post_request(self, arrangement: dict[str, object]) -> Any:
        return self._client.post(USER_REGISTER_URL, arrangement)

    def _then_should_create_user(self, result: Any) -> None:
        expected_status_code = status.HTTP_201_CREATED

        self.assertEqual(expected_status_code, result.status_code)
        self.assertNotIn("password", result.data)
        self.assertEqual(result.data.get("first_name"), "Tom")
