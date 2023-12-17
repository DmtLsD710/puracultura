# Importamos la función 'path' y el módulo 'views' desde el paquete 'django.urls'
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views

# Definimos el nombre de la aplicación como 'core'
app_name = 'core'

# Configuramos las URL para la aplicación 'core'
urlpatterns = [
    # Definimos una ruta vacía que corresponde a la página de inicio
    # y asociamos la función 'frontpage' de 'views' a esta ruta
    path('', views.frontpage, name='home'),
]