from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.gis.db.models.functions import Distance, Area
from django.contrib.gis.geos import GEOSGeometry, Point
from rest_framework.decorators import action, api_view
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
            return Response(item.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @api_view(['GET'])
    def read_items(self, request):
        if request.query_params:
            items = Building.objects.filter(**request.query_param.dict())
        else:
            items = Building.objects.all()

        if items:
            data = BuildingSerializer(items)
            return Response(data)
        Response(status=status.HTTP_404_NOT_FOUND)
        '''queryset = Building.objects.all()
        serialize = BuildingSerializer(queryset, many=True)
        return Response(serialize.data)'''

    @api_view(['POST'])
    def update_item(self, request, pk=None):
        item = Building.objects.get(pk=pk)
        data = BuildingSerializer(instance=item, data=request.data)
        if data.is_valid():
            data.save()
            return Response(data.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @api_view(['DELETE'])
    def destroy(self, request, pk=None):
        item = get_object_or_404(Building, pk=pk)
        item.delete()
        return Response(status=status.HTTP_202_ACCEPTED)

    # Выдает объекты, с площадью, попадающей в диапазон от min до max
    @action(detail=False, methods=['get'])
    def get_obj_in_area(self, request):
        min_area = request.GET.get('min', None)
        max_area = request.GET.get('max', None)
        if min_area or max_area:
            query_set = Building.objects.all()
            if min_area:
                query_set = query_set.annotate(Area('geom') > min_area)
            if max_area:
                query_set = query_set.annotate(Area('geom') < max_area)
            serializer = self.get_serializer_class()
            serialized = serializer(query_set, many=True)
            print(query_set)
            return Response(serialized.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # Выдает объекты, попадающие в окружность с центром в x, y и радиусом distance
    #     point = Point(-80.191788, 25.761681, srid=4326)
    @action(detail=False, methods=['get'])
    def get_obj_in_radius(self, request):  # queryset, value, point, distance):
        x_coords = request.GET.get('x', None)
        y_coords = request.GET.get('y', None)
        distance = request.GET.get('dist', None)
        if x_coords and y_coords and distance:
            point = Point(float(x_coords), float(y_coords), srid=4326)
            query_set = Building.objects.annotate(distance=Distance('geom', point)).order_by('distance')[0:distance]
            serializer = self.get_serializer_class()
            serialized = serializer(query_set, many=True)
            print(query_set)
            return Response(serialized.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
