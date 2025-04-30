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
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    chofer = models.ForeignKey(Chofer, on_delete=models.CASCADE)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Solo validar si es una nueva asignación
            # Validar que el vehículo no esté ya asignado
            if Asignacion.objects.filter(vehiculo=self.vehiculo, fecha_modificacion__isnull=True).exists():
                raise ValueError("Este vehículo ya está asignado a un chofer.")
            # Validar que el chofer no esté ya asignado
            if Asignacion.objects.filter(chofer=self.chofer, fecha_modificacion__isnull=True).exists():
                raise ValueError("Este chofer ya está asignado a un vehículo.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.chofer.nombre_completo} -> {self.vehiculo.placa}'
