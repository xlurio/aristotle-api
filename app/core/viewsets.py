from django.utils.decorators import method_decorator
from rest_framework import mixins, viewsets
from core.constants import TimeMeasure
from django.views.decorators.vary import vary_on_headers
from django.views.decorators.cache import cache_page


class WriteOnlyViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """Interface for creating write only view sets"""


class ReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    """Interface for creating read only view sets"""

    @method_decorator(cache_page(2 * TimeMeasure.HOUR))
    @method_decorator(vary_on_headers("Authorization"))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @method_decorator(cache_page(2 * TimeMeasure.HOUR))
    @method_decorator(vary_on_headers("Authorization"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
