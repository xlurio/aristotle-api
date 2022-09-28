from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser

from core import viewsets
from user_register.api import serializers


class UserViewSet(viewsets.WriteOnlyViewSet):
    """User registering endpoint"""

    serializer_class = serializers.UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
