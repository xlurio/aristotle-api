from core import viewsets
from grade_register.api.serializers import GradeSerializer


class GradeViewSet(viewsets.WriteOnlyViewSet):
    """Write only end point for registering grades"""

    serializer_class = GradeSerializer
