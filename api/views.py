from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view
from django_filters import rest_framework as filters

from .models import Building
from .serializer import BuildingSerializer
from .filters import BuildingFilters


class BuildingView(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    filterset_class = BuildingFilters
    filter_backends = [filters.DjangoFilterBackend]

    @api_view(['POST'])
    def create_item(self, request):
        item = BuildingSerializer(data=request.data)
        if item.is_valid():
            item.save()
            return item.data

    @api_view(['GET'])
    def read_items(self, request):
        if request.query_params:
            items = Building.objects.filter(**request.query_param.dict())
        else:
            items = Building.objects.all()
        return items

    @api_view(['POST'])
    def update_item(self, request, pk=None):
        item = Building.objects.get(pk=pk)
        data = BuildingSerializer(instance=item, data=request.data)
        if data.is_valid():
            data.save()
            return data.data
        return data.data

    @api_view(['DELETE'])
    def destroy(self, request, pk=None):
        item = get_object_or_404(Building, pk=pk)
        item.delete()
