from core import viewsets, models
from classroom_creation.api.serializers import ClassRoomSerializer


class ClassRoomViewSet(viewsets.WriteOnlyViewSet):
    """End point for creating new class rooms"""

    serializer_class = ClassRoomSerializer
