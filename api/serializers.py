# serializers.py
from rest_framework import serializers
from .models import Vehiculo
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
