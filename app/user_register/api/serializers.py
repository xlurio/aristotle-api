import uuid
from user_register.services import generate_registry
from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    role_choices = (
        ("staff", "Staff"),
        ("student", "Student"),
        ("teacher", "Teacher"),
    )

    registry = serializers.CharField(read_only=True)

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
        model = get_user_model()
        fields = ["registry", "first_name", "last_name", "password", "role"]

    def create(self, validated_data):
        creation_method_dict = {
            "student": get_user_model().objects.create_student,
            "teacher": get_user_model().objects.create_professor,
            "staff": get_user_model().objects.create_superuser,
        }

        role = validated_data.pop("role")
        print(validated_data)

        registry = generate_registry()

        return creation_method_dict.get(role)(
            registry=registry,
            **validated_data,
        )
