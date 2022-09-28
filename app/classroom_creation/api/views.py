from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser

from classroom_creation.api.serializers import ClassRoomSerializer
from core import viewsets


class ClassRoomViewSet(viewsets.WriteOnlyViewSet):
    """End point for creating new class rooms"""

    serializer_class = ClassRoomSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]
