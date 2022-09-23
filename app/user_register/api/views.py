from core import viewsets
from user_register.api import serializers


class UserViewSet(viewsets.WriteOnlyViewSet):
    """User registering endpoint"""

    serializer_class = serializers.UserSerializer
