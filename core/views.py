from django.shortcuts import render
from item.models import Category, Item

def frontpage(request):
    
    items = Item.objects.filter(stock__gt=0)[0:6]
    categories = Category.objects.all()
    
    return render(request, 'core/frontpage.html',{
        'categories': categories,
        'items': items,
    })
