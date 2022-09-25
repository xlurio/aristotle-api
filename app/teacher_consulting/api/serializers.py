from rest_framework import serializers

from core.models import (
    AbsenceDate,
    ClassRoomDetails,
    GradeDetails,
    ReadOnlyAbsence,
    ReadOnlyClassroom,
    ReadOnlyGrade,
    Student,
    Teacher,
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
    """Serializer for the absence dates date"""

    class Meta:
        """Absence detail serializer meta data"""

        model = AbsenceDate
        fields = ["absence_date"]


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


class ClassroomDetailSerializer(serializers.ModelSerializer):
    """Serializer for the class room detailed data"""

    subject = serializers.CharField(max_length=254, read_only=True)
    students = StudentSerializer(many=True, read_only=True)

    class Meta:
        """Class room detailed data serializer meta data"""

        model = ClassRoomDetails
        fields = ["subject", "students"]


class ClassroomSerializer(serializers.ModelSerializer):
    """Serializer for the class room data"""

    class Meta:
        model = ReadOnlyClassroom
        fields = ["classroom_id", "name"]


class TeacherSerializer(serializers.ModelSerializer):
    """Serializer for the teacher data"""

    classrooms = ClassroomSerializer(many=True, read_only=True)

    class Meta:
        model = Teacher
        fields = ["teacher", "classrooms"]
