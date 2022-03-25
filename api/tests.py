from django.test import TestCase
from django.contrib.gis.geos import Polygon

from .models import Building
from .filters import BuildingFilters


class BuindingFiltersTestCase(TestCase):
    def setUp(self):
        Building.objects.create(geom=Polygon([(0.0, 0.0), (0.0, 50.0), (50.0, 50.0), (50.0, 0.0)], (0.0, 0.0), ),
                                address='344091')
        Building.objects.create(geom=Polygon([(36.0, 0.0), (20.0, 1.0), (-9.0, 50.0), (0.0, 0.0), (36.0, 0.0)]),
                                address='666591')
        Building.objects.create(geom=Polygon([(20.0, 0.0), (0.0, 50.0), (30.0, -5.0), (20.0, 0.0)]),
                                address='544472')

    # Есть только максимальная площадь
    def test_filter_area_max(self):
        response = self.client.get('/api/buildings/4/')
        self.assertEqual(response.data,
                         Building(geom=Polygon([(0.0, 0.0), (0.0, 50.0), (50.0, 50.0), (50.0, 0.0)], (0.0, 0.0), ),
                                  address='344091'))

    # Есть только минимальная площадь
    def test_filter_area_min(self):
        pass

    # Площадь от мин до макс
    def test_filter_area(self):
        pass

    # Попадает внутрь окружности
    def test_filter_distance_in(self):
        pass

    # Не попадает внутрь окружности
    def test_filter_distance(self):
        pass
