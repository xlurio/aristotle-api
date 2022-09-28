from rest_framework import serializers

from core.models import (
    AbsenceDetail,
    ClassroomAbsence,
    ClassroomGrade,
    GradeDetail,
    StudentClassroom,
)


class GradeDetailSerializer(serializers.ModelSerializer):
    """Serializer for the grade detailed data"""

    class Meta:
        """Grade value serializer meta data"""

        model = GradeDetail
        fields = ["title", "grade_value"]


class GradeSerializer(serializers.ModelSerializer):
    """Serializer for the grade data"""

    grade_values = GradeDetailSerializer(many=True, read_only=True)

    class Meta:
        """Grade serializer meta data"""

        model = ClassroomGrade
        fields = ["average", "grade_values"]


class AbsenceDetailSerializer(serializers.ModelSerializer):
    """Serializer for the absence detailed data"""

    class Meta:
        """Absence detail serializer meta data"""

        model = AbsenceDetail
        fields = ["absence_date"]


class AbsenceSerializer(serializers.ModelSerializer):
    """Serializer for the absence data"""

    absence_dates = AbsenceDetailSerializer(many=True, read_only=True)

    class Meta:
        """Absence serializer meta data"""

        model = ClassroomAbsence
        fields = ["absence_amount", "frequency", "absence_dates"]


class StudentClassroomSerializer(serializers.ModelSerializer):
    """Seriazer for the student data"""

    grades = GradeSerializer(many=True, read_only=True)
    absences = AbsenceSerializer(many=True, read_only=True)

    class Meta:
        """Student serializer meta data"""

        model = StudentClassroom
        fields = ["id", "student", "grades", "absences"]
