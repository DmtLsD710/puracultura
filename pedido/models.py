from django.db import models
from django.conf import settings
from item.models import Item
from userprofile.models import Direccion

class Pedido(models.Model):
    ESTADO_OPCIONES = [
        ('en proceso', 'En Proceso'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    actualizacion = models.DateTimeField(auto_now=True)
    estado = models.CharField(max_length=20, choices=ESTADO_OPCIONES, default='en proceso')
    costo_total = models.FloatField()
    direccion_envio = models.ForeignKey(Direccion, on_delete=models.SET_NULL, null=True)
    

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Item, on_delete=models.CASCADE)
    precio = models.FloatField()
    cantidad = models.IntegerField()
    
    