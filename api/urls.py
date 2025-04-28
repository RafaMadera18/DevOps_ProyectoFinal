# urls.py
from django.urls import path
from .views import VehiculoCreateView

urlpatterns = [
    path('api/vehiculos/', VehiculoCreateView.as_view(), name='vehiculo-create'),
]
