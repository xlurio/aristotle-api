from rest_framework import viewsets, authentication
from django.db.models.query import QuerySet
from core.models import Student
from student_consulting.permissions import IsStudent
from student_consulting.api.serializers import StudentSerializer


class StudentViewSet(viewsets.ReadOnlyModelViewSet):
    """Student data view"""

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsStudent]
    serializer_class = StudentSerializer

    def get_queryset(self) -> QuerySet[Student]:
        return Student.objects.filter(user_id=self.request.user.id)
