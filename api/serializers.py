# serializers.py
from rest_framework import serializers
from .models import Vehiculo
from .models import Chofer
from .models import Asignacion
from .models import Ruta
from .models import Administrador

import re

class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = '__all__'

    def validate_vin(self, value):
        if len(value) != 17:
            raise serializers.ValidationError("El número de serie (VIN) debe tener exactamente 17 caracteres.")
        if not re.match(r'^[A-HJ-NPR-Z0-9]+$', value):  # excluye I, O, Q
            raise serializers.ValidationError("El VIN contiene caracteres inválidos.")
        return value

    def validate_placa(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("La placa debe tener al menos 6 caracteres.")
        if not re.match(r'^[A-Z0-9\-]+$', value, re.IGNORECASE):
            raise serializers.ValidationError("La placa solo puede contener letras, números y guiones.")
        return value
    
class ChoferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chofer
        fields = '__all__'

    def validate_curp(self, value):
        if len(value) != 18:
            raise serializers.ValidationError("El CURP debe tener 18 caracteres.")
        if not re.match(r'^[A-Z]{4}\d{6}[HM][A-Z]{5}[A-Z\d]{2}$', value, re.IGNORECASE):
            raise serializers.ValidationError("El CURP no tiene un formato válido.")
        return value

    def validate_numero_licencia(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("El número de licencia debe tener al menos 5 caracteres.")
        if not re.match(r'^[A-Z0-9\-]+$', value, re.IGNORECASE):
            raise serializers.ValidationError("La licencia solo puede contener letras, números y guiones.")
        return value

    def validate_salario_mensual(self, value):
        if value <= 0:
            raise serializers.ValidationError("El salario mensual debe ser mayor que cero.")
        return value    

class AsignacionSerializer(serializers.ModelSerializer):
    activa = serializers.ReadOnlyField()

    class Meta:
        model = Asignacion
        fields = ['id', 'chofer', 'vehiculo', 'fecha_asignacion', 'fecha_modificacion', 'activa']
        read_only_fields = ['fecha_modificacion', 'fecha_asignacion', 'activa']

class RutaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ruta
        fields = '__all__'

    def validate(self, data):
        vehiculo = data['vehiculo']
        chofer = data['chofer']
        fecha = data['fecha_recorrido']

        # Validar que el vehículo no tenga otra ruta en la misma fecha
        if Ruta.objects.filter(vehiculo=vehiculo, fecha_recorrido=fecha).exists():
            raise serializers.ValidationError({
                "detalle": "Este vehículo ya tiene una ruta asignada para esa fecha."
            })

        # Verificar que exista una asignación activa entre el vehículo y el chofer
        asignacion_activa = Asignacion.objects.filter(
            vehiculo=vehiculo,
            chofer=chofer,
            fecha_modificacion__isnull=True
        ).first()

        if not asignacion_activa:
            raise serializers.ValidationError({
                "detalle": "No existe una asignación activa entre el chofer y el vehículo."
            })

        return data
    
class RegistroAdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Administrador
        fields = ['id', 'email', 'codigo_invitacion', 'password']
        read_only_fields = ['codigo_invitacion']

    def create(self, validated_data):
        validated_data.pop('codigo_invitacion', None)
        return Administrador.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
