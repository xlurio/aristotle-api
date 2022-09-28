from rest_framework import mixins, viewsets


class WriteOnlyViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """Interface for creating read only view sets"""
