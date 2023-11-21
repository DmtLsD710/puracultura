from django.urls import path

from . import views

# Definimos el nombre de la aplicación, que se usará para hacer referencia a estas URLs desde otras partes de Django
app_name = 'item'

# Definimos las URLs para esta aplicación
urlpatterns = [
    # La URL 'new/' está asociada con la vista 'new'. Esto significa que cuando un usuario visita 'item/new/', Django ejecutará la función de vista 'new'.
    path('new/', views.new, name='new'),
    # La URL '<int:pk>/' está asociada con la vista 'detail'. Esto significa que cuando un usuario visita 'item/1/', por ejemplo, Django ejecutará la función de vista 'detail' con 'pk' igual a 1.
    path('<int:pk>/', views.detail, name='detail'),
]