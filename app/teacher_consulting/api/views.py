from rest_framework import viewsets, authentication
from core.models import Teacher
from teacher_consulting.api.serializers import TeacherSerializer
from teacher_consulting.permissions import IsTeacher


class TeacherViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = TeacherSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsTeacher]

    def get_queryset(self):
        return Teacher.objects.filter(user_id=self.request.user.id)
