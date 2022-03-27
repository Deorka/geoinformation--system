from django.test import TestCase
from django.contrib.gis.geos import Polygon, GEOSGeometry

from .models import Building


class BuindingFiltersTestCase(TestCase):
    def setUp(self):
        p1 = GEOSGeometry(
            'POLYGON ((-98.503358 29.335668, -98.503086 29.335668, -98.503086 29.335423, -98.503358 29.335423, -98.503358 29.335668))',
            srid=4326)
        self.building1 = Building.objects.create(geom=p1, address="666666")
        p2 = GEOSGeometry('POLYGON ((0 0, 0 50, 50 50, 50 0, 0 0))', srid=4326)
        self.building2 = Building.objects.create(geom=p2, address='344091')
        p3 = GEOSGeometry('POLYGON ((100 0, 101 0, 101 1, 100 1, 100 0))', srid=4326)
        self.building3 = Building.objects.create(geom=p3, address='665471')
        p4 = GEOSGeometry('POLYGON ((4 0, 0 0, 0 4, 4 4, 4 0))', srid=4326)
        self.building4 = Building.objects.create(geom=p4, address='444444')
        p5 = GEOSGeometry('POLYGON ((-99 29, -99 28, -98 28, -99 29))', srid=4326)
        self.building5 = Building.objects.create(geom=p5, address='999999')

    # Есть только максимальная площадь
    def test_filter_area_max(self):
        response = self.client.get('/api/buildings/?max=10000000000')  # /api/buildings/?max=1000
        self.assertEqual(len(response.data['features']), 2)
        self.assertEqual(Polygon(response.data['features'][0]['geometry']['coordinates'][0], srid=4326),
                         self.building1.geom)
        self.assertEqual(Polygon(response.data['features'][1]['geometry']['coordinates'][0], srid=4326),
                         self.building5.geom)
        response = self.client.get('/api/buildings/?max=1000')
        self.assertEqual(len(response.data['features']), 1)
        self.assertEqual(Polygon(response.data['features'][0]['geometry']['coordinates'][0], srid=4326),
                         self.building1.geom)

    # Есть только минимальная площадь
    def test_filter_area_min(self):
        response = self.client.get('/api/buildings/?min=10000000000')
        self.assertEqual(len(response.data['features']), 3)
        self.assertEqual(Polygon(response.data['features'][0]['geometry']['coordinates'][0], srid=4326),
                         self.building2.geom)
        self.assertEqual(Polygon(response.data['features'][1]['geometry']['coordinates'][0], srid=4326),
                         self.building3.geom)
        self.assertEqual(Polygon(response.data['features'][2]['geometry']['coordinates'][0], srid=4326),
                         self.building4.geom)
        response = self.client.get('/api/buildings/?min=196869599070.80536')
        self.assertEqual(len(response.data['features']), 2)
        self.assertEqual(Polygon(response.data['features'][0]['geometry']['coordinates'][0], srid=4326),
                         self.building2.geom)
        self.assertEqual(Polygon(response.data['features'][1]['geometry']['coordinates'][0], srid=4326),
                         self.building4.geom)
        response = self.client.get('/api/buildings/?min=dta')
        self.assertEqual(response.status_code, 400)

    # Площадь от мин до макс
    def test_filter_area(self):
        response = self.client.get('/api/buildings/?min=100000000&max=10000000000')
        self.assertEqual(len(response.data['features']), 1)
        self.assertEqual(Polygon(response.data['features'][0]['geometry']['coordinates'][0], srid=4326),
                         self.building5.geom)
        response = self.client.get('/api/buildings/?min=1111111&max=1111111')
        self.assertEqual(len(response.data['features']), 0)
        response = self.client.get('/api/buildings/?min=0&max=99999999999999')
        self.assertEqual(len(response.data['features']), 5)
        response = self.client.get('/api/buildings/?min=-9&max=gaga')
        self.assertEqual(response.status_code, 400)

    # Попадает внутрь окружности
    def test_filter_distance_in(self):
        response = self.client.get('/api/buildings/?x=0&y=1&dist=4000000')
        self.assertEqual(len(response.data['features']), 2)
        self.assertEqual(Polygon(response.data['features'][0]['geometry']['coordinates'][0], srid=4326),
                         self.building2.geom)
        self.assertEqual(Polygon(response.data['features'][1]['geometry']['coordinates'][0], srid=4326),
                         self.building4.geom)
        response = self.client.get('/api/buildings/?x=-99&y=29&dist=100')
        self.assertEqual(len(response.data['features']), 1)
        self.assertEqual(Polygon(response.data['features'][0]['geometry']['coordinates'][0], srid=4326),
                         self.building5.geom)
        response = self.client.get('/api/buildings/?x=50&y=50&dist=1234567890')
        self.assertEqual(len(response.data['features']), 5)

    # Не попадает внутрь окружности
    def test_filter_distance(self):
        response = self.client.get('/api/buildings/?x=60&y=10&dist=100')
        self.assertEqual(len(response.data['features']), 0)
        response = self.client.get('/api/buildings/?x=0&y=1&dist=-100')
        self.assertEqual(response.status_code, 400)
        response = self.client.get('/api/buildings/?x=165&y=-100&dist=10000')
        self.assertEqual(len(response.data['features']), 0)
