from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import DjangoModelPermissions

from core import viewsets
from core.models import Grade
from grade_register.api.serializers import GradeSerializer


class GradeViewSet(viewsets.WriteOnlyViewSet):
    """Write only end point for registering grades"""

    serializer_class = GradeSerializer
    queryset = Grade.objects.all()
    permission_classes = [DjangoModelPermissions]
    authentication_classes = [TokenAuthentication]
