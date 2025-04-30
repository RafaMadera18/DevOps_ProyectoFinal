# views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
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

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import Asignacion, Chofer, Vehiculo
from .serializers import AsignacionSerializer

class AsignacionViewSet(viewsets.ModelViewSet):
    queryset = Asignacion.objects.all()
    serializer_class = AsignacionSerializer

    def create(self, request, *args, **kwargs):
        chofer_id = request.data.get('chofer')
        vehiculo_id = request.data.get('vehiculo')

        if not chofer_id or not vehiculo_id:
            return Response({"error": "chofer y vehiculo son requeridos"}, status=400)

        try:
            chofer = Chofer.objects.get(pk=chofer_id)
        except Chofer.DoesNotExist:
            return Response({"chofer": "El chofer no existe."}, status=400)

        try:
            vehiculo = Vehiculo.objects.get(pk=vehiculo_id)
        except Vehiculo.DoesNotExist:
            return Response({"vehiculo": "El vehículo no existe."}, status=400)

        # Verificar si ya existe una asignación activa idéntica
        if Asignacion.objects.filter(chofer=chofer, vehiculo=vehiculo, fecha_modificacion__isnull=True).exists():
            return Response({"detalle": "Esta asignación ya está activa."}, status=200)

        # Desactivar asignaciones activas del chofer
        Asignacion.objects.filter(chofer=chofer, fecha_modificacion__isnull=True).update(fecha_modificacion=timezone.now())

        # Desactivar asignaciones activas del vehículo
        Asignacion.objects.filter(vehiculo=vehiculo, fecha_modificacion__isnull=True).update(fecha_modificacion=timezone.now())

        # Crear nueva asignación
        nueva = Asignacion.objects.create(chofer=chofer, vehiculo=vehiculo)
        serializer = self.get_serializer(nueva)
        return Response(serializer.data, status=status.HTTP_201_CREATED)