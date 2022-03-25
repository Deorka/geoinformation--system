from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.contrib.gis.db.models.functions import Distance, Area
from django.contrib.gis.geos import Point

from .models import Building
from .serializer import BuildingSerializer


class BuildingView(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    # filter_backends = [filters.DjangoFilterBackend]

    @api_view(['POST'])
    def create_item(self, request):
        item = BuildingSerializer(data=request.data)
        if item.is_valid():
            item.save()
            return item.data

    @api_view(['POST'])
    def update_item(self, request, pk=None):
        item = Building.objects.get(pk=pk)
        data = BuildingSerializer(instance=item, data=request.data)
        if data.is_valid():
            data.save()
        return data.data

    @api_view(['DELETE'])
    def destroy(self, request, pk=None):
        item = get_object_or_404(Building, pk=pk)
        item.delete()

    @api_view(['GET'])
    def read_items(self, request):
        min_area = request.GET.get('min', None)
        max_area = request.GET.get('max', None)
        x_coords = request.GET.get('x', None)
        y_coords = request.GET.get('y', None)
        distance = request.GET.get('dist', None)

        query_set = Building.objects.all()
        if min_area or max_area:
            query_set = self.filter_obj_in_area(query_set, min_area, max_area)
        if x_coords and y_coords and distance:
            query_set = self.filter_obj_in_radius(query_set, x_coords, y_coords, distance)
        serializer = BuildingSerializer(query_set, many=True)
        return JsonResponse(serializer.data, safe=False)

    # Выдает объекты, с площадью, попадающей в диапазон от min до max
    def filter_obj_in_area(self, query_set, min_area, max_area):
        if min_area:
            query_set = query_set.annotate(Area('geom') > min_area)
        if max_area:
            query_set = query_set.annotate(Area('geom') < max_area)
        return query_set

    # Выдает объекты, попадающие в окружность с центром в x, y и радиусом distance
    def filter_obj_in_radius(self, query_set, x_coords, y_coords, distance):
        point = Point(float(x_coords), float(y_coords), srid=4326)
        return query_set.annotate(distance=Distance('geom', point)).order_by('distance')[0:distance]
