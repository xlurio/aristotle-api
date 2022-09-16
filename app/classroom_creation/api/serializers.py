from typing import Any
from rest_framework import serializers
from core.models import ClassRoom
from classroom_creation.services import ClassRoomFactory
from django.contrib.auth import get_user_model


class ClassRoomSerializer(serializers.ModelSerializer):
    """Serializes the class room objects"""

    name = serializers.ReadOnlyField()
    members = serializers.PrimaryKeyRelatedField(
        many=True, queryset=get_user_model().objects.all()
    )

    class Meta:
        """Class room serializer meta data"""

        model = ClassRoom
        fields = "__all__"

    def create(self, validated_data: Any) -> ClassRoom:
        """Creates a class room with the request data and returns it

        Args:
            validated_data (Any): the request data

        Returns:
            ClassRoom: the created classroom
        """

        factory = ClassRoomFactory()
        return factory.make_classroom(**validated_data)
