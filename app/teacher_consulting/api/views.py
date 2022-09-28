from django.db.models import QuerySet
from rest_framework import authentication

from core.models import ClassRoom, TeacherClassroom
from core.viewsets import ReadOnlyViewSet
from teacher_consulting.api.serializers import TeacherClassroomSerializer
from teacher_consulting.permissions import IsTeacher


class TeacherViewSet(ReadOnlyViewSet):

    serializer_class = TeacherClassroomSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsTeacher]

    def get_queryset(self) -> QuerySet[TeacherClassroom]:
        classrooms: QuerySet[ClassRoom] = ClassRoom.objects.filter(
            members__id=self.request.user.id
        )
        classrooms_id: list[int] = [classroom.id for classroom in classrooms]

        teacher_classrooms: QuerySet[
            TeacherClassroom
        ] = TeacherClassroom.objects.filter(classroom_id__in=classrooms_id)

        return teacher_classrooms.order_by("id")
