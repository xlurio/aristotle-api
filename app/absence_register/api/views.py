from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import DjangoModelPermissions

from absence_register.api.serializers import AbsenceSerializer
from core import viewsets
from core.models import Absence


class AbsenceViewSet(viewsets.WriteOnlyViewSet):
    """Write only end point for registering absences"""

    serializer_class = AbsenceSerializer
    queryset = Absence.objects.all()
    permission_classes = [DjangoModelPermissions]
    authentication_classes = [TokenAuthentication]
