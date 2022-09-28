from typing import Any, Dict

from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.models import User
from user_register.services import UserFactory


class UserSerializer(serializers.ModelSerializer):
    """Serializes the user objects"""

    role_choices = (("student", "Student"), ("teacher", "Teacher"), ("staff", "Staff"))

    register = serializers.CharField(default="", style={"input_type": "hidden"})

    password = serializers.CharField(
        required=True,
        write_only=True,
        style={"input_type": "password"},
    )

    role = serializers.ChoiceField(
        required=True,
        write_only=True,
        choices=role_choices,
    )

    class Meta:
        """User serializer meta data"""

        model = get_user_model()
        fields = ["register", "first_name", "last_name", "password", "role"]

    def create(self, validated_data: Dict[str, Any]) -> User:
        """Creates a new user and return it

        Args:
            validated_data (Dict[str, Any]): the request data

        Returns:
            User: the new user
        """
        factory = UserFactory()
        return factory.make_user(**validated_data)
