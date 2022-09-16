from rest_framework import viewsets, mixins


class WriteOnlyViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """Interface for creating read only view sets"""
