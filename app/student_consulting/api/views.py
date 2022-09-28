from django.db.models.query import QuerySet
from rest_framework import authentication

from core.models import StudentClassroom
from core.viewsets import ReadOnlyViewSet
from student_consulting.api.serializers import StudentClassroomSerializer
from student_consulting.permissions import IsStudent


class StudentViewSet(ReadOnlyViewSet):
    """Student data view"""

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsStudent]
    serializer_class = StudentClassroomSerializer

    def get_queryset(self) -> QuerySet[StudentClassroom]:
        classrooms: QuerySet[StudentClassroom] = StudentClassroom.objects.filter(
            user_id=self.request.user.id
        )
        return classrooms.order_by("id")
