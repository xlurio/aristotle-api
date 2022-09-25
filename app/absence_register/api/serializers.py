from typing import Any
from rest_framework import serializers
from core import models
from absence_register.services import AbsenceFactory, ReadOnlyAbsenceFactory
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
        new_absence = factory.make_absence(**validated_data)

        read_only_factory = ReadOnlyAbsenceFactory(new_absence)
        new_read_only_absence = read_only_factory.make_absence()
        new_read_only_absence.save()

        return new_absence
