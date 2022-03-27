from django.db.models.expressions import RawSQL
from rest_framework import viewsets
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import Building
from .serializer import BuildingSerializer


class BuildingView(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer

    def list(self, request, *args, **kwargs):
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
        return Response(serializer.data)

    # Выдает объекты, с площадью, попадающей в диапазон от min до max
    def filter_obj_in_area(self, query_set, min_area, max_area):
        query_set = query_set.annotate(area=RawSQL("ST_AREA(geom,true)", []))
        validate_positive_number(max_area)
        validate_positive_number(min_area)
        if min_area:
            min_area = float(min_area)
            query_set = query_set.filter(area__gte=min_area)
            if max_area:
                max_area = float(max_area)
                if max_area > min_area:
                    query_set = query_set.filter(area__lte=max_area)
        elif max_area:
            max_area = float(max_area)
            query_set = query_set.filter(area__lte=max_area)
        return query_set

    # Выдает объекты, попадающие в окружность с центром в x, y и радиусом distance
    def filter_obj_in_radius(self, query_set, x_coords, y_coords, distance):
        point = Point(float(x_coords), float(y_coords), srid=4326)
        validate_positive_number(distance)
        distance = float(distance)
        if distance > 0:
            return query_set.annotate(distance=Distance('geom', point)).filter(distance__lt=distance)


def validate_positive_number(value):
    if value:
        try:
            value = float(value)
            if value < 0:
                raise ValidationError("Negative value entered! Positive value required!")
        except Exception:
            raise ValidationError("String entered! Need a positive value!")
