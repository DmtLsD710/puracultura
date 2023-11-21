from django.shortcuts import render
from item.models import Category, Item

def frontpage(request):
    # Filtrar los objetos de la clase Item cuyo stock sea mayor que cero y obtener los primeros 6 elementos
    items = Item.objects.filter(stock__gt=0)[0:6]
    # Obtener todos los objetos de la clase Category
    categories = Category.objects.all()
    
    # Renderizar la plantilla 'core/frontpage.html' con los datos de las categorías y los elementos obtenidos
    return render(request, 'core/frontpage.html',{
        'categories': categories,
        'items': items,
    })
