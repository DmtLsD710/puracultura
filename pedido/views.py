from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Pedido, ItemPedido, Direccion, Item
from item.cart import Cart
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import F 

@login_required
def resumen_pedido(request):
    cart = Cart(request)
    direcciones = Direccion.objects.filter(usuario=request.user)
    if request.method == 'POST':
        direccion_id = request.POST.get('direccion')
        direccion = get_object_or_404(Direccion, id=direccion_id)
        return render(request, 'confirmar_pedido.html', {
            'cart': cart,
            'IVA': cart.get_IVA(),
            'direccion': direccion,
        })
    else:
        return render(request, 'pedido/resumen_pedido.html', {
            'cart': cart,
            'direcciones': direcciones,
        })

@login_required
def confirmar_compra(request):
    cart = Cart(request)
    if request.method == 'POST':
        direccion_id = request.POST.get('direccion')
        direccion = get_object_or_404(Direccion, id=direccion_id)

        # Initialize a dictionary to hold orders by vendor
        orders_by_vendor = {}

        # Iterate over items in the cart
        for item_id, item_data in cart.cart.items():
            item = Item.objects.get(id=item_id)
            vendor_id = item.created_by.id

            # Add the item to the vendor's order
            if vendor_id not in orders_by_vendor:
                orders_by_vendor[vendor_id] = {
                    'pedido': None,
                    'items': [],
                    'total': 0
                }

            orders_by_vendor[vendor_id]['items'].append(item)
            orders_by_vendor[vendor_id]['total'] += item.price * item_data['quantity']

        # Create an order for each vendor
        for vendor_id, data in orders_by_vendor.items():
            pedido = Pedido.objects.create(
                usuario=request.user,
                estado='En proceso',
                costo_total=data['total'],
                direccion_envio=direccion
            )
            data['pedido'] = pedido

            # Create an ItemPedido for each item
            for item in data['items']:
                quantity = cart.cart[str(item.id)]['quantity']
                ItemPedido.objects.create(
                    pedido=pedido,
                    producto=item,
                    precio=item.price,
                    cantidad=quantity,
                )
                # Update stock
                item.stock -= quantity
                item.save()

        cart.clear()
        return redirect('core:home')
    else:
        return redirect('item:cart_view')


@login_required
def cancelar_compra(request):
    return redirect('item:cart_view')

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Pedido, ItemPedido, Direccion, Item
from item.cart import Cart
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

@login_required
def resumen_pedido(request):
    cart = Cart(request)
    direcciones = Direccion.objects.filter(usuario=request.user)
    if request.method == 'POST':
        direccion_id = request.POST.get('direccion')
        direccion = get_object_or_404(Direccion, id=direccion_id)
        return render(request, 'confirmar_pedido.html', {
            'cart': cart,
            'IVA': cart.get_IVA(),
            'direccion': direccion,
        })
    else:
        return render(request, 'pedido/resumen_pedido.html', {
            'cart': cart,
            'direcciones': direcciones,
        })

@login_required
def confirmar_compra(request):
    cart = Cart(request)
    if request.method == 'POST':
        direccion_id = request.POST.get('direccion')
        direccion = get_object_or_404(Direccion, id=direccion_id)

        # Initialize a dictionary to hold orders by vendor
        orders_by_vendor = {}

        # Iterate over items in the cart
        for item_id, item_data in cart.cart.items():
            item = Item.objects.get(id=item_id)
            vendor_id = item.created_by.id

            # Add the item to the vendor's order
            if vendor_id not in orders_by_vendor:
                orders_by_vendor[vendor_id] = {
                    'pedido': None,
                    'items': [],
                    'total': 0
                }

            orders_by_vendor[vendor_id]['items'].append(item)
            orders_by_vendor[vendor_id]['total'] += item.price * item_data['quantity']

        # Create an order for each vendor
        for vendor_id, data in orders_by_vendor.items():
            pedido = Pedido.objects.create(
                usuario=request.user,
                estado='En proceso',
                costo_total=data['total'],
                direccion_envio=direccion
            )
            data['pedido'] = pedido

            # Create an ItemPedido for each item
            for item in data['items']:
                quantity = cart.cart[str(item.id)]['quantity']
                ItemPedido.objects.create(
                    pedido=pedido,
                    producto=item,
                    precio=item.price,
                    cantidad=quantity,
                )
                # Update stock
                item.stock -= quantity
                item.save()

        cart.clear()
        return redirect('core:home')
    else:
        return redirect('item:cart_view')

@login_required
def cancelar_compra(request):
    return redirect('item:cart_view')

@login_required
def historial_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user).annotate(
        vendedor_name=F('itempedido__producto__created_by__username')
    ).order_by('-fecha_creacion')
    
    paginator = Paginator(pedidos, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'pedido/historial_pedidos.html', {'page_obj': page_obj})


@login_required
def historial_pedidos_vendedor(request):
    pedidos_vendedor = Pedido.objects.filter(
        itempedido__producto__created_by=request.user
    ).distinct().order_by('-fecha_creacion')

    paginator = Paginator(pedidos_vendedor, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pedido/historial_pedidos_vendedor.html', {'page_obj': page_obj})

@login_required
def actualizar_estado_pedido(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)
    if request.method == 'POST' and pedido.itempedido_set.first().producto.created_by == request.user:
        nuevo_estado = request.POST.get('estado')
        pedido.estado = nuevo_estado
        pedido.save()
    return HttpResponseRedirect(reverse('pedido:historial_pedidos_vendedor'))