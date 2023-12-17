from django.shortcuts import render, redirect, get_object_or_404
from .models import Pedido, ItemPedido, Direccion
from item.cart import Cart

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

def confirmar_compra(request):
    if request.method == 'POST':
        cart = Cart(request)
        direccion_id = request.POST.get('direccion')
        direccion = get_object_or_404(Direccion, id=direccion_id)


        pedido = Pedido.objects.create(
            usuario=request.user,
            estado='En proceso',
            costo_total=cart.get_total_cost(),
            direccion_envio=direccion,
        )

        for item in cart:
            producto = item['product']
            cantidad = item['quantity']
            ItemPedido.objects.create(
                pedido=pedido,
                producto=producto,
                precio=producto.price,
                cantidad=cantidad,
            )
            producto.stock = max(producto.stock - cantidad, 0)
            producto.save()

        cart.clear()
        
    return redirect('core:home')

def cancelar_compra(request):
    return redirect('item:cart_view')
