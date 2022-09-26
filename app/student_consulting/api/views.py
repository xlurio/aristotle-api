from rest_framework import viewsets, authentication
from django.db.models.query import QuerySet
from core.models import StudentClassroom
from student_consulting.permissions import IsStudent
from student_consulting.api.serializers import StudentClassroomSerializer


class StudentViewSet(viewsets.ReadOnlyModelViewSet):
    """Student data view"""

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsStudent]
    serializer_class = StudentClassroomSerializer

    def get_queryset(self) -> QuerySet[StudentClassroom]:
        return StudentClassroom.objects.filter(user_id=self.request.user.id)
