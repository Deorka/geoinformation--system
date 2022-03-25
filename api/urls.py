from django.urls import path, include
from rest_framework import routers

from .views import BuildingView

router = routers.DefaultRouter()
router.register('buildings', BuildingView)

urlpatterns = [
    path('', include(router.urls)),

]
