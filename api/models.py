from django.db import models
from django.utils import timezone

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
    
class Chofer(models.Model):
    nombre_completo = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    curp = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    salario_mensual = models.DecimalField(max_digits=10, decimal_places=2)
    numero_licencia = models.CharField(max_length=100)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.nombre_completo} - {self.numero_licencia}'

class Asignacion(models.Model):
    chofer = models.ForeignKey(Chofer, on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    fecha_asignacion = models.DateField(auto_now_add=True)
    fecha_modificacion = models.DateField(null=True, blank=True)

    @property
    def activa(self):
        return self.fecha_modificacion is None

    def __str__(self):
        estado = "Activa" if self.activa else f"Finalizada el {self.fecha_modificacion}"
        return f"{self.chofer} asignado a {self.vehiculo} desde {self.fecha_asignacion} ({estado})"

class Ruta(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_recorrido = models.DateField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    exitosa = models.BooleanField(default=True)
    descripcion_problema = models.TextField(blank=True)
    comentarios = models.TextField(blank=True)

    # Ubicación de origen (empresa) y destino
    latitud_origen = models.DecimalField(max_digits=9, decimal_places=6)
    longitud_origen = models.DecimalField(max_digits=9, decimal_places=6)
    latitud_destino = models.DecimalField(max_digits=9, decimal_places=6)
    longitud_destino = models.DecimalField(max_digits=9, decimal_places=6)

    # Relaciones
    vehiculo = models.ForeignKey('Vehiculo', on_delete=models.PROTECT)
    chofer = models.ForeignKey('Chofer', on_delete=models.PROTECT)

    class Meta:
        unique_together = ('vehiculo', 'fecha_recorrido')  # 1 ruta por día por vehículo

    def __str__(self):
        return f"{self.nombre} - {self.fecha_recorrido}"