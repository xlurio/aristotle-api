from core import viewsets
from absence_register.api.serializers import AbsenceSerializer
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.authentication import TokenAuthentication


class AbsenceViewSet(viewsets.WriteOnlyViewSet):
    """Write only end point for registering absences"""

    serializer_class = AbsenceSerializer
    permission_classes = [DjangoModelPermissions]
    authentication_classes = [TokenAuthentication]
