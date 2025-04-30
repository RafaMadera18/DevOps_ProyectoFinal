# serializers.py
from rest_framework import serializers
from .models import Vehiculo
from .models import Chofer
from .models import Asignacion

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
    class Meta:
        model = Asignacion
        fields = '__all__'
        read_only_fields = ['fecha_modificacion']

    def validate(self, data):
        persona = data.get('persona')
        vehiculo = data.get('vehiculo')
        instance = self.instance  # Será None si es un POST, no None si es PUT/PATCH

        # Validar existencia explícitamente (opcional si ForeignKey ya hace esto)
        if not Chofer.objects.filter(pk=persona.pk).exists():
            raise serializers.ValidationError({"persona": "El chofer no existe."})
        if not Vehiculo.objects.filter(pk=vehiculo.pk).exists():
            raise serializers.ValidationError({"vehiculo": "El vehículo no existe."})

        # Validar que no haya otra asignación activa para ese chofer
        chofer_activo = Asignacion.objects.filter(persona=persona, fecha_modificacion__isnull=True)
        if instance:
            chofer_activo = chofer_activo.exclude(pk=instance.pk)
        if chofer_activo.exists():
            raise serializers.ValidationError({"persona": "Este chofer ya tiene una asignación activa."})

        # Validar que no haya otra asignación activa para ese vehículo
        vehiculo_activo = Asignacion.objects.filter(vehiculo=vehiculo, fecha_modificacion__isnull=True)
        if instance:
            vehiculo_activo = vehiculo_activo.exclude(pk=instance.pk)
        if vehiculo_activo.exists():
            raise serializers.ValidationError({"vehiculo": "Este vehículo ya está asignado a otro chofer."})

        return data
