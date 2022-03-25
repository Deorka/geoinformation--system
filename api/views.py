from django.db.models.expressions import RawSQL
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django.http import JsonResponse
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point

from .models import Building
from .serializer import BuildingSerializer


class BuildingView(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer

    def list(self, request):
        min_area = request.GET.get('min', None)
        max_area = request.GET.get('max', None)
        x_coords = request.GET.get('x', None)
        y_coords = request.GET.get('y', None)
        distance = request.GET.get('dist', None)

        query_set = self.queryset
        if min_area or max_area:
            query_set = self.filter_obj_in_area(query_set, min_area, max_area)
        if x_coords and y_coords and distance:
            query_set = self.filter_obj_in_radius(query_set, x_coords, y_coords, distance)
        serializer = BuildingSerializer(query_set, many=True)
        return JsonResponse(serializer.data, safe=False)

    # Выдает объекты, с площадью, попадающей в диапазон от min до max
    def filter_obj_in_area(self, query_set, min_area, max_area):
        query_set = query_set.annotate(area=RawSQL("ST_AREA(geom,true)", []))
        if min_area:
            query_set = query_set.filter(area__gt=float(min_area))
        if max_area:
            query_set = query_set.filter(area__lt=float(max_area))
        return query_set

    # Выдает объекты, попадающие в окружность с центром в x, y и радиусом distance
    def filter_obj_in_radius(self, query_set, x_coords, y_coords, distance):
        point = Point(float(x_coords), float(y_coords), srid=4326)
        return query_set.annotate(distance=Distance('geom', point)).order_by('distance')[0:int(distance)]
