from core import viewsets, models
from absence_register.api.serializers import AbsenceSerializer


class AbsenceViewSet(viewsets.WriteOnlyViewSet):
    """Write only end point for registering absences"""

    serializer_class = AbsenceSerializer
