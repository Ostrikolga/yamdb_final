from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .permissions import IsAdminOrReadOnly


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """ ViewSet помогающий."""

    pass
