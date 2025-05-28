# views.py
from rest_framework import viewsets, status, serializers, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Vehiculo
from .models import Chofer
from .models import Asignacion
from .models import Ruta
from .models import Administrador

from .serializers import VehiculoSerializer
from .serializers import ChoferSerializer
from .serializers import AsignacionSerializer
from .serializers import RutaSerializer
from .serializers import RegisterAdminSerializer

class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

class ChoferViewSet(viewsets.ModelViewSet):
    queryset = Chofer.objects.all()
    serializer_class = ChoferSerializer
    permission_classes = [IsAuthenticated]

class AsignacionViewSet(viewsets.ModelViewSet):
    queryset = Asignacion.objects.all()
    serializer_class = AsignacionSerializer
    permission_classes = [IsAuthenticated]

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
    
class RutaViewSet(viewsets.ModelViewSet):
    queryset = Ruta.objects.all()
    serializer_class = RutaSerializer
    permission_classes = [IsAuthenticated]

class AdministradorViewSet(viewsets.ModelViewSet):
    queryset = Administrador.objects.all()
    serializer_class = RegisterAdminSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        # Bloquear creación desde aquí
        return Response({'detail': 'No permitido crear administradores desde este endpoint.'},
                        status=405)  # 405 Method Not Allowed

class AdminTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        if not self.user.is_staff:
            raise serializers.ValidationError("Solo los administradores pueden iniciar sesión.")
        return data

class AdminTokenObtainPairView(TokenObtainPairView):
    serializer_class = AdminTokenObtainPairSerializer

class RegisterAdminView(APIView):
    def post(self, request):
        serializer = RegisterAdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Administrador registrado con éxito.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class FatalErrorView(APIView):
    def get(self, request, *args, **kwargs):
        # Esto provoca una excepción fatal
        raise RuntimeError("Error fatal de prueba generado intencionalmente.")