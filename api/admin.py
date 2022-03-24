from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from .models import Building


@admin.register(Building)
class BuildingAdmin(OSMGeoAdmin):
    list_display = ('address', 'geom')
