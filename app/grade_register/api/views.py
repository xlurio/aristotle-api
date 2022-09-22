from core import viewsets
from grade_register.api.serializers import GradeSerializer
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.authentication import TokenAuthentication


class GradeViewSet(viewsets.WriteOnlyViewSet):
    """Write only end point for registering grades"""

    serializer_class = GradeSerializer
    permission_classes = [DjangoModelPermissions]
    authentication_classes = [TokenAuthentication]
