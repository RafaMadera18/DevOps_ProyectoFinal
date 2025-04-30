# views.py
from rest_framework import viewsets
from .models import Vehiculo
from .models import Chofer
from .models import Asignacion


from .serializers import VehiculoSerializer
from .serializers import ChoferSerializer
from .serializers import AsignacionSerializer

class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer

class ChoferViewSet(viewsets.ModelViewSet):
    queryset = Chofer.objects.all()
    serializer_class = ChoferSerializer

class AsignacionViewSet(viewsets.ModelViewSet):
    queryset = Asignacion.objects.all()
    serializer_class = AsignacionSerializer
