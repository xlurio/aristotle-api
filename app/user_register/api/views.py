from rest_framework import viewsets, mixins
from django.contrib.auth import get_user_model
from user_register.api import serializers


class UserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """User registering endpoint"""

    serializer_class = serializers.UserSerializer
    queryset = get_user_model()

    def perform_create(self, serializer):
        serializer.save()
