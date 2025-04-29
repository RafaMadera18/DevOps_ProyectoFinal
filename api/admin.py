from django.contrib import admin
from .models import Vehiculo
from .models import Chofer

# Register your models here.

admin.site.register(Vehiculo)
admin.site.register(Chofer)