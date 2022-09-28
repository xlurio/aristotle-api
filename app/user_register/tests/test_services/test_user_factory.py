from django.test import TestCase

from core.models import User
from user_register.services import UserFactory


class UserFactoryTests(TestCase):
    """Test for the user factory"""

    def test_make_student(self) -> None:
        """test case description"""
        arrangement = self._given_user_data("student")
        result = self._when_user_made(arrangement)
        self._then_should_create_student(result)

    def _then_should_create_student(self, result: User) -> None:
        is_user_allowed_to_view_grade = result.has_perm("core.view_grade")
        is_user_allowed_to_change_grade = result.has_perm("core.change_grade")
        is_user_student = (
            is_user_allowed_to_view_grade and not is_user_allowed_to_change_grade
        )

        self.assertTrue(is_user_student)

    def test_make_teacher(self) -> None:
        """Test creating teacher"""
        arrangement = self._given_user_data("teacher")
        result = self._when_user_made(arrangement)
        self._then_should_create_teacher(result)

    def _then_should_create_teacher(self, result: User) -> None:
        is_user_allowed_to_change_absence = result.has_perm("core.change_absence")
        is_user_allowed_to_change_grade = result.has_perm("core.change_grade")
        is_user_teacher = (
            is_user_allowed_to_change_absence and is_user_allowed_to_change_grade
        )

        self.assertTrue(is_user_teacher)

    def test_make_staff(self) -> None:
        """Test creating staff"""
        arrangement = self._given_user_data("staff")
        result = self._when_user_made(arrangement)
        self._then_should_create_staff(result)

    def _then_should_create_staff(self, result: User) -> None:
        self.assertTrue(result.is_staff)

    def _given_user_data(self, role: str) -> dict[str, object]:
        first_name = "Tom"
        last_name = "Cruise"
        password = "12345"

        return {
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
            "role": role,
        }

    def _when_user_made(self, arrangement: dict[str, object]) -> User:
        factory = UserFactory()

        return factory.make_user(**arrangement)
