from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.frontpage, name='home'),
    path('terms/', views.terms, name='terms'),
]