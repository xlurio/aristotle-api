from rest_framework import viewsets, authentication
from core.models import ClassRoom
from core.models import TeacherClassroom
from teacher_consulting.api.serializers import TeacherClassroomSerializer
from teacher_consulting.permissions import IsTeacher
from django.db.models import QuerySet


class TeacherViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = TeacherClassroomSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsTeacher]

    def get_queryset(self) -> QuerySet[TeacherClassroom]:
        classrooms: QuerySet[ClassRoom] = ClassRoom.objects.filter(
            members__id=self.request.user.id
        )
        classrooms_id: list[int] = [classroom.id for classroom in classrooms]

        return TeacherClassroom.objects.filter(classroom_id__in=classrooms_id)
