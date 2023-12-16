from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
from .cart import Cart
from .forms import NewItemForm
from .models import Item, Category

from django.core.paginator import Paginator

# Detail view for a single item
def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, stock__gt=0).exclude(pk=pk)[:3]
    
    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items
    })

# View for adding a new item
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

# Dashboard view to list all items for the current seller
@login_required
def dashboard(request):
    if not request.user.vendedor:
        return redirect('core:home')

    items = Item.objects.filter(created_by=request.user)
    return render(request, 'item/dashboard.html', {'items': items})

# View for editing an existing item
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
        'item': item,  # Pass the item to the template for additional context (optional)
    })

# Function to delete an item
@login_required
def delete_item(request, pk):
    if not request.user.vendedor:
        return redirect('core:home')

    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    if request.method == 'POST':
        item.delete()
        return redirect('item:dashboard')  # Redirect to the dashboard after deletion
    return render(request, 'item/delete_confirm.html', {
        'item': item
    })

def search(request):
    query = request.GET.get('query', '')
    item = Item.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    
    paginator = Paginator(item, 20) # Show 20 items per page.
    
    page_number = request.GET.get('page')
    item = paginator.get_page(page_number)
    
    return render(request, 'item/search.html', {
        'query': query,
        'item': item
    })    
    
def category_detail(request, pk): 
    category = get_object_or_404(Category, pk=pk)
    items = category.items.all()
    
    paginator = Paginator(items, 20) # Show 20 items per page.

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
    