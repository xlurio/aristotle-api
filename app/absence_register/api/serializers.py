from typing import Any
from rest_framework import serializers
from core import models
from absence_register.services import AbsenceFactory
from django.contrib.auth import get_user_model


class AbsenceSerializer(serializers.ModelSerializer):
    """Serializer for absence objects"""

    classroom = serializers.PrimaryKeyRelatedField(
        queryset=models.ClassRoom.objects.all()
    )
    student = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all()
    )

    class Meta:
        """Absence serializer meta data"""

        model = models.Absence
        fields = "__all__"

    def create(self, validated_data: Any) -> models.Absence:
        factory = AbsenceFactory()
        return factory.make_absence(**validated_data)
