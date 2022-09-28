from typing import Any

from django.contrib.auth import get_user_model
from rest_framework import serializers

from core import models
from grade_register.services import GradeFactory, ReadOnlyGradeFactory


class GradeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    student = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all()
    )
    classroom = serializers.PrimaryKeyRelatedField(
        queryset=models.ClassRoom.objects.all()
    )

    class Meta:
        model = models.Grade
        fields = ["id", "title", "grade", "student", "classroom"]

    def create(self, validated_data: Any) -> models.Grade:
        factory = GradeFactory()
        new_grade = factory.make_grade(**validated_data)

        read_only_factory = ReadOnlyGradeFactory(new_grade)
        new_read_only_grade = read_only_factory.make_grade()
        new_read_only_grade.save()

        return new_grade
