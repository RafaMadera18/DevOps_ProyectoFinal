from django.db import models

# Create your models here.

class Vehiculo(models.Model):
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    vin = models.CharField(max_length=100, unique=True)
    placa = models.CharField(max_length=50, unique=True)
    fecha_compra = models.DateField()
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    fotografia = models.ImageField(upload_to='vehiculos_fotos/')
    fecha_ingreso = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.marca} {self.modelo} - {self.placa}'