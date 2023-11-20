from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

validar_cedula = RegexValidator(regex='^[0-9]+$', message='La cédula debe contener solo números', code='cedula_invalida')
validar_telefono = RegexValidator(regex='^[0-9]+$', message='El teléfono debe contener solo números', code='telefono_invalido')

class Usuario(AbstractUser):
    vendedor = models.BooleanField(default=False)
    biografia = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    cedula = models.CharField(max_length=9, unique=True, validators=[validar_cedula])
    telefono = models.CharField(max_length=15, unique=True, validators=[validar_telefono])

class Direccion(models.Model):
    usuario = models.ForeignKey(Usuario, related_name='direcciones', on_delete=models.CASCADE)
    direccion = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=20)

    def __str__(self):
        return self.direccion
