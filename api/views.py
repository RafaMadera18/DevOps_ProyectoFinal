# views.py
from rest_framework import viewsets
from .models import Vehiculo
from .models import Chofer

from .serializers import VehiculoSerializer
from .serializers import ChoferSerializer


class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer

class ChoferViewSet(viewsets.ModelViewSet):
    queryset = Chofer.objects.all()
    serializer_class = ChoferSerializer