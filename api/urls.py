# urls.py
from django.urls import path, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'vehiculos', views.VehiculoViewSet, basename='vehiculos')
router.register(r'choferes', views.ChoferViewSet, basename='choferes')
router.register(r'asignaciones', views.AsignacionViewSet, basename='asignaciones')
router.register(r'rutas', views.RutaViewSet, basename='rutas')


urlpatterns = [
    path('', include(router.urls)),
]