from rest_framework_gis.filterset import GeoFilterSet
from django.contrib.gis.db.models.functions import Distance, Area
from django.contrib.gis.geos import Point
from rest_framework.decorators import action

from .models import Building


class BuildingFilters(GeoFilterSet):
    class Meta:
        model = Building
        exclude = ['geom']

    # Выдает объекты, с площадью, попадающей в диапазон от min до max
    @action(detail=False, methods=['get'])
    def filter_obj_in_area(self, request):
        min_area = request.GET.get('min', None)
        max_area = request.GET.get('max', None)
        query_set = Building.objects.all()
        if min_area or max_area:
            if min_area:
                query_set = query_set.annotate(Area('geom') > min_area)
            if max_area:
                query_set = query_set.annotate(Area('geom') < max_area)
            return query_set
        else:
            return query_set

    # Выдает объекты, попадающие в окружность с центром в x, y и радиусом distance
    @action(detail=False, methods=['get'])
    def filter_obj_in_radius(self, request):  # queryset, value, point, distance):
        x_coords = request.GET.get('x', None)
        y_coords = request.GET.get('y', None)
        distance = request.GET.get('dist', None)
        if x_coords and y_coords and distance:
            point = Point(float(x_coords), float(y_coords), srid=4326)
            return Building.objects.annotate(distance=Distance('geom', point)).order_by('distance')[0:distance]
        else:
            return Building.objects.all()
