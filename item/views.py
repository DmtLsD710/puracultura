# Importamos los módulos necesarios de Django
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

# Importamos el formulario NewItemForm y el modelo Item de nuestros módulos locales
from .forms import NewItemForm
from .models import Item

# Definimos la vista 'detail'
def detail(request, pk):
    # Obtenemos el item con la clave primaria 'pk', o lanzamos un error 404 si no existe
    item = get_object_or_404(Item, pk=pk)
    # Obtenemos los items relacionados que pertenecen a la misma categoría y tienen stock, excluyendo el item actual
    related_items = Item.objects.filter(category=item.category, stock__gt=0 ).exclude(pk=pk)[0:3]
    
    # Renderizamos la plantilla 'item/detail.html' con el item y los items relacionados
    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items
        })
    
    
# Definimos la vista 'new', que requiere que el usuario esté autenticado
@login_required
def new(request):
    # Si el usuario no es un vendedor, lo redirigimos a la página de inicio
    if not request.user.vendedor:
        return redirect('core:home') 

    # Si la solicitud es un POST, procesamos el formulario
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)
        
        # Si el formulario es válido, guardamos el item y lo asociamos con el usuario actual
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            
            # Redirigimos al usuario a la página de detalles del item
            return redirect('item:detail', pk=item.id)
    # Si la solicitud no es un POST, mostramos el formulario vacío
    else:
        form = NewItemForm()
        
    # Renderizamos la plantilla 'item/form.html' con el formulario y el título
    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Nuevo Producto',
    })   