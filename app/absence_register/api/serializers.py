from typing import Any

from django.contrib.auth import get_user_model
from rest_framework import serializers

from absence_register.services import AbsenceFactory, ReadOnlyAbsenceFactory
from core import models


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
        fields = ["absence_date", "classroom", "student"]

    def create(self, validated_data: Any) -> models.Absence:
        factory = AbsenceFactory()
        new_absence = factory.make_absence(**validated_data)

        read_only_factory = ReadOnlyAbsenceFactory(new_absence)
        absence_classroom = read_only_factory.make_absence()
        absence_classroom.save()

        return new_absence
