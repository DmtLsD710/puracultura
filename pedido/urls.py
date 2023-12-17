from django.urls import path
from . import views

app_name = 'pedido'  

urlpatterns = [
    path('resumen/', views.resumen_pedido, name='resumen_pedido'),
    path('confirmar/', views.confirmar_compra, name='confirmar_compra'),
    path('cancelar/', views.cancelar_compra, name='cancelar_compra'),
    
]
