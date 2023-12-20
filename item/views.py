from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q, F
from .cart import Cart
from .forms import NewItemForm
from .models import Item, Category

from django.core.paginator import Paginator


def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, stock__gt=0).exclude(pk=pk)[:3]
    
    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items
    })


@login_required
def new(request):
    if not request.user.vendedor:
        return redirect('core:home') 

    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()
    
    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Nuevo Producto',
    })


@login_required
def dashboard(request):
    if not request.user.vendedor:
        return redirect('core:home')

    items = Item.objects.filter(created_by=request.user)
    return render(request, 'item/dashboard.html', {'items': items})


@login_required
def edit_item(request, pk):
    if not request.user.vendedor:
        return redirect('core:home')

    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item:detail', pk=item.pk)
    else:
        form = NewItemForm(instance=item)
    
    return render(request, 'item/edit_item.html', {
        'form': form,
        'title': 'Editar Producto',
        'item': item,  
    })

@login_required
def delete_item(request, pk):
    if not request.user.vendedor:
        return redirect('core:home')

    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    if request.method == 'POST':
        item.delete()
        return redirect('item:dashboard')  
    return render(request, 'item/delete_confirm.html', {
        'item': item
    })

def search(request):
    query = request.GET.get('query', '')
    sort_option = request.GET.get('sort', '')

    items = Item.objects.filter(Q(name__icontains=query) | Q(description__icontains=query), stock__gt=0)

    if sort_option == 'asc':
        items = items.order_by('price')
    elif sort_option == 'desc':
        items = items.order_by(F('price').desc())

    paginator = Paginator(items, 10)

    page_number = request.GET.get('page')
    item = paginator.get_page(page_number)

    return render(request, 'item/search.html', {
        'query': query,
        'item': item
    })

    
def category_detail(request, pk): 
    category = get_object_or_404(Category, pk=pk)
    items = Item.objects.filter(category=category, stock__gt=0) 
    
    paginator = Paginator(items, 10)

    page_number = request.GET.get('page')
    items = paginator.get_page(page_number)
    
    return render(request, 'item/category_detail.html', {
        'category': category,
        'items': items
    })

@login_required   
def add_to_cart(request, item_id):
    cart = Cart(request)
    cart.add(item_id)

    return redirect('item:cart_view')

@login_required
def remove_from_cart(request, item_id):
    cart = Cart(request)
    cart.remove(item_id)

    return redirect('item:cart_view')
@login_required
def cart_view(request):
    cart = Cart(request)

    return render(request, 'item/cart_view.html', {
        'cart': cart
    })
    
@login_required
def increase_quantity(request, item_id):
    cart = Cart(request)
    cart.add(item_id, quantity=1)  
    return redirect('item:cart_view')

@login_required
def decrease_quantity(request, item_id):
    cart = Cart(request)
    cart.add(item_id, quantity=-1) 
    return redirect('item:cart_view')
    