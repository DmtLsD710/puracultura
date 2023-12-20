from django.urls import path
from . import views

app_name = 'pedido'  

urlpatterns = [
    path('resumen/', views.resumen_pedido, name='resumen_pedido'),
    path('confirmar/', views.confirmar_compra, name='confirmar_compra'),
    path('cancelar/', views.cancelar_compra, name='cancelar_compra'),
    path('historial_vendedor/', views.historial_pedidos_vendedor, name='historial_pedidos_vendedor'),
    path('historial/', views.historial_pedidos, name='historial_pedidos'),
    path('actualizar/<int:pedido_id>/', views.actualizar_estado_pedido, name='actualizar_estado'),
    
]
