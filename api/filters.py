from rest_framework_gis.filterset import GeoFilterSet
from rest_framework_gis.filters import GeometryFilter
from django_filters import filters
from .models import Building

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import GEOSGeometry, Point
from rest_framework.decorators import action
from django_filters import rest_framework as filters


class BuildingFilters(GeoFilterSet):
    geom_obj = filters.CharFilter(method='get_geo_objects')

    class Meta:
        model = Building
        exclude = ['geom']

    def get_geo_objects(self, queryset, value):
        query_set = Building.objects.filter(pk=value)
        if query_set:
            obj = query_set.first()
            return queryset.filter(geom__within=obj.geom)
        return queryset


