from rest_framework import viewsets, authentication
from core.models import TeacherClassroom
from teacher_consulting.api.serializers import TeacherClassroomSerializer
from teacher_consulting.permissions import IsTeacher
from django.db.models import QuerySet


class TeacherViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = TeacherClassroomSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsTeacher]

    def get_queryset(self) -> QuerySet[TeacherClassroom]:
        return TeacherClassroom.objects.filter(user_id=self.request.user.id)
