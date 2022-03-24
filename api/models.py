from django.db import models
from django.contrib.gis.db import models


class Building(models.Model):
    geom = models.PolygonField(null=True, blank=True)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.address

    class Meta:
        managed = False
        db_table = 'building'
