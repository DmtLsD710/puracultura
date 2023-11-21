from django.contrib import admin

from .models import Category, Item, Review

# Registra los modelos Category, Item y Review en el sitio de administración de Django
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Review)