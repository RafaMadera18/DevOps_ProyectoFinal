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

class AsignacionViewSet(viewsets.ModelViewSet):
    queryset = Asignacion.objects.all()
    serializer_class = AsignacionSerializer

    @action(detail=False, methods=['post'], url_path='reasignar')
    def reasignar(self, request):
        chofer_id = request.data.get('chofer')
        vehiculo_id = request.data.get('vehiculo')

        try:
            chofer = Chofer.objects.get(pk=chofer_id)
            vehiculo = Vehiculo.objects.get(pk=vehiculo_id)
        except Chofer.DoesNotExist:
            return Response({"error": "Chofer no existe"}, status=status.HTTP_400_BAD_REQUEST)
        except Vehiculo.DoesNotExist:
            return Response({"error": "Vehículo no existe"}, status=status.HTTP_400_BAD_REQUEST)

        # Cerrar asignaciones activas del chofer y vehículo
        hoy = timezone.now().date()
        Asignacion.objects.filter(chofer=chofer, fecha_modificacion__isnull=True).update(fecha_modificacion=hoy)
        Asignacion.objects.filter(vehiculo=vehiculo, fecha_modificacion__isnull=True).update(fecha_modificacion=hoy)

        # Crear nueva asignación
        nueva = Asignacion.objects.create(
            chofer=chofer,
            vehiculo=vehiculo,
            fecha_asignacion=hoy
        )
        serializer = self.get_serializer(nueva)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
