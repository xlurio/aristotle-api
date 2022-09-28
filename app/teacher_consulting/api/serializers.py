from rest_framework import serializers

from core.models import (
    AbsenceDetail,
    ClassroomAbsence,
    ClassroomGrade,
    ClassroomStudent,
    GradeDetail,
    TeacherClassroom,
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


class ClassroomStudentsSerializer(serializers.ModelSerializer):
    """Serializer for the classroom student data"""

    grades = GradeSerializer(many=True, read_only=True)
    absence = AbsenceSerializer(many=True, read_only=True)

    class Meta:
        """Class room student serializer meta data"""

        model = ClassroomStudent
        fields = ["student", "grades", "absence"]


class TeacherClassroomSerializer(serializers.ModelSerializer):
    """Serializer for the teacher class room data"""

    students = ClassroomStudentsSerializer(many=True, read_only=True)

    class Meta:
        """Teacher class room serializer meta data"""

        model = TeacherClassroom
        fields = ["id", "classroom", "students"]
