from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import (ListModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from onlinefem.fem.models import FEM
from .serializers import FEMSerializer


class FEMViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin,
                 GenericViewSet):
    serializer_class = FEMSerializer
    queryset = FEM.objects.all()

    def get_queryset(self, *args, **kwargs):
        return self.queryset

    @action(detail=False, methods=["GET"])
    def fem(self, request):
        serializer = FEMSerializer()
        return Response(status=status.HTTP_200_OK, data=serializer.data)
