# views.py
from rest_framework import generics
from .models import Vehiculo
from .serializers import VehiculoSerializer
from rest_framework.permissions import IsAuthenticated

class VehiculoCreateView(generics.CreateAPIView):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    permission_classes = [IsAuthenticated]
