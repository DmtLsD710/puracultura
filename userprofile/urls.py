from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

# Definimos el nombre de la aplicación, que se utilizará para referenciar estas URLs en otras partes del código
app_name = 'userprofile'

# Definimos las URLs de la aplicación
urlpatterns = [
    # La URL 'signup/' está asociada con la vista 'signup_view' y tiene el nombre 'signup'
    path('signup/', views.signup_view, name='signup'),
    # La URL 'login/' está asociada con la vista 'login_view' y tiene el nombre 'login'
    path('login/', views.login_view, name='login'),
    # La URL 'logout/' está asociada con la vista 'LogoutView' y tiene el nombre 'logout'
    # 'LogoutView.as_view(next_page='/')' crea una vista basada en clase que redirige al usuario a la página de inicio después de cerrar sesión
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]