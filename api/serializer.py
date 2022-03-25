from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import Building


class BuildingSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Building
        fields = ('geom', 'address')
        geo_field = 'geom'
        read_only_fields = ['distance']
