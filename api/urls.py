from django.urls import path, include
from django.contrib import admin
from rest_framework import routers
from .views import BuildingView

router = routers.DefaultRouter()
router.register(r'buildingview', BuildingView)

urlpatterns = [
    path('', include(router.urls)),
    #path('buildings/', BuildingView.as_view({'get': 'get'}))  # need as_view() {'get': 'retrieve'}
    path('buildings/', include('rest_framework.urls', namespace='rest_framework')),
    path('create/', BuildingView.create_item, name='create_item'),
    path('all/', BuildingView.read_items, name='read_items'),
    path('update/<int:pk>/', BuildingView.update_item, name='update_item'),

]
