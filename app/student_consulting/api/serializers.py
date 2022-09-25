from dataclasses import fields
from rest_framework import serializers
from core.models import (
    AbsenceDate,
    GradeDetails,
    ReadOnlyAbsence,
    ReadOnlyGrade,
    Student,
)


class GradeDetailsSerializer(serializers.ModelSerializer):
    """Serializer for the grade detailed data"""

    class Meta:
        """Grade value serializer meta data"""

        model = GradeDetails
        fields = ["title", "grade_value"]


class GradeSerializer(serializers.ModelSerializer):
    """Serializer for the grade data"""

    grade_values = GradeDetailsSerializer(many=True, read_only=True)

    class Meta:
        """Grade serializer meta data"""

        model = ReadOnlyGrade
        fields = ["classroom", "average", "grade_values"]


class AbsenceDateSerializer(serializers.ModelSerializer):
    """Serializer for the absence dates data"""

    class Meta:
        """Absence detail serializer meta data"""

        model = AbsenceDate
        fields = ["absence_data"]


class AbsenceSerializer(serializers.ModelSerializer):
    """Serializer for the absence data"""

    absence_dates = AbsenceDateSerializer(many=True, read_only=True)

    class Meta:
        """Absence serializer meta data"""

        model = ReadOnlyAbsence
        fields = ["class_room", "absence_amount", "frequency", "absence_dates"]


class StudentSerializer(serializers.ModelSerializer):
    """Seriazer for the student data"""

    grades = GradeSerializer(many=True, read_only=True)
    absences = AbsenceSerializer(many=True, read_only=True)

    class Meta:
        """Student serializer meta data"""

        model = Student
        fields = ["student", "grades", "absences"]
