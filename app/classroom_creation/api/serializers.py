from typing import Any

from django.contrib.auth import get_user_model
from rest_framework import serializers

from classroom_creation.services import ClassRoomFactory
from core.models import ClassRoom


class ClassRoomSerializer(serializers.ModelSerializer):
    """Serializes the class room objects"""

    id = serializers.ReadOnlyField()
    name = serializers.ReadOnlyField()
    members = serializers.PrimaryKeyRelatedField(
        many=True, queryset=get_user_model().objects.all()
    )

    class Meta:
        """Class room serializer meta data"""

        model = ClassRoom
        fields = [
            "id",
            "subject",
            "name",
            "members",
            "school_days",
            "start",
            "deadline",
        ]

    def create(self, validated_data: Any) -> ClassRoom:
        """Creates a class room with the request data and returns it

        Args:
            validated_data (Any): the request data

        Returns:
            ClassRoom: the created classroom
        """

        factory = ClassRoomFactory()
        return factory.make_classroom(**validated_data)
