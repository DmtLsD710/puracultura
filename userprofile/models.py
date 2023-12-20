from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Definición de validadores personalizados para cédula y teléfono
validar_cedula = RegexValidator(regex='^[0-9]+$', message='La cédula debe contener solo números', code='cedula_invalida')
validar_telefono = RegexValidator(regex='^[0-9]+$', message='El teléfono debe contener solo números', code='telefono_invalido')

class Usuario(AbstractUser):
    # Modelo de usuario personalizado que hereda de AbstractUser
    vendedor = models.BooleanField(default=False)  # Campo booleano para indicar si el usuario es vendedor o no
    biografia = models.TextField(blank=True, null=True)  # Campo de texto para la biografía del usuario
    fecha_registro = models.DateTimeField(auto_now_add=True)  # Campo de fecha y hora para el registro del usuario
    cedula = models.CharField(max_length=9, unique=True, validators=[validar_cedula])  # Campo de texto para la cédula del usuario con validador personalizado
    telefono = models.CharField(max_length=15, unique=True, validators=[validar_telefono])  # Campo de texto para el teléfono del usuario con validador personalizado

class Direccion(models.Model):
    # Modelo de dirección asociado a un usuario
    usuario = models.ForeignKey(Usuario, related_name='direcciones', on_delete=models.CASCADE)  # Relación de clave foránea con el modelo Usuario
    direccion = models.CharField(max_length=255)  # Campo de texto para la dirección
    ciudad = models.CharField(max_length=100)  # Campo de texto para la ciudad
    pais = models.CharField(max_length=100)  # Campo de texto para el país
    codigo_postal = models.CharField(max_length=20)  # Campo de texto para el código postal

    def __str__(self):
        return f"{self.direccion}, {self.ciudad}, {self.pais}, {self.codigo_postal}"
