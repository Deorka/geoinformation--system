from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers, viewsets
from rest_framework.response import Response

from .models import Building


class BuildingSerializer(GeoFeatureModelSerializer):
    distance = serializers.CharField()

    class Meta:
        model = Building
        fields = ('geom', 'address')
        geo_field = 'geom'
        read_only_fields = ['distance']
