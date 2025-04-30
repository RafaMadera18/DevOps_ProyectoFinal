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
    activa = serializers.ReadOnlyField()

    class Meta:
        model = Asignacion
        fields = ['id', 'chofer', 'vehiculo', 'fecha_asignacion', 'fecha_modificacion', 'activa']
        read_only_fields = ['fecha_modificacion', 'fecha_asignacion', 'activa']
