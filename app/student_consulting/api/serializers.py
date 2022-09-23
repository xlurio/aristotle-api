from rest_framework import serializers


class GradeDetailSerializer(serializers.Serializer):
    """Serializer for the grade details"""

    title = serializers.CharField(max_length=254, read_only=True)
    grade = serializers.IntegerField(read_only=True)


class GradeSerializer(serializers.Serializer):
    """Serializer for the grade objects"""

    class_room = serializers.CharField(max_length=254, read_only=True)
    grades = GradeDetailSerializer(many=True, read_only=True)


class AbsenceSerializer(serializers.Serializer):
    """Serializer for the absence objects"""

    class_room = serializers.CharField(max_length=254, read_only=True)
    absence_amount = serializers.IntegerField(read_only=True)
    frequency = serializers.FloatField(read_only=True)
    absence_dates = serializers.DateField(read_only=True)


class StudentSerializer(serializers.Serializer):
    """Serializer for the student data"""

    student = serializers.CharField(max_length=254, read_only=True)
    grades = GradeSerializer(many=True, read_only=True)
    absences = AbsenceSerializer(many=True, read_only=True)
