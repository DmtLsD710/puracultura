from django.db.models import Count, Q
from django.shortcuts import render
from item.models import Category, Item

def frontpage(request):
    items = Item.objects.filter(stock__gt=0)[0:6]
    categories = Category.objects.annotate(
        num_items_in_stock=Count('items', filter=Q(items__stock__gt=0))
    ).filter(num_items_in_stock__gt=0)
    
    return render(request, 'core/frontpage.html',{
        'categories': categories,
        'items': items,
    })

def terms(request):
    return render(request, 'core/terms.html')