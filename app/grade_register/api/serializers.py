from typing import Any
from rest_framework import serializers
from core import models
from grade_register.services import GradeFactory
from django.contrib.auth import get_user_model


class GradeSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all()
    )
    classroom = serializers.PrimaryKeyRelatedField(
        queryset=models.ClassRoom.objects.all()
    )

    class Meta:
        model = models.Grade
        fields = "__all__"

    def create(self, validated_data: Any) -> models.Grade:
        factory = GradeFactory()
        return factory.make_grade(**validated_data)
