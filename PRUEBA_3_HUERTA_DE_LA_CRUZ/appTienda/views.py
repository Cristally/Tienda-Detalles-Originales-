from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Pedido
from .forms import SolicitudPedidoForm
from django.contrib import messages

def Base(request):
    return render(request, "base.html")

def catalogo(request):
    productos = Producto.objects.all()
    return render(request, 'catalogo.html', {'productos': productos})

def crear_pedido(request):
    token_generado = None
    if request.method == 'POST':
        form = SolicitudPedidoForm(request.POST, request.FILES)
        if form.is_valid():
            pedido = form.save() # Se guarda y genera el token automático
            token_generado = pedido.token_seguimiento
            messages.success(request, f'¡Pedido recibido! Tu código de seguimiento es: {token_generado}')
            # Opcional: Redirigir o quedarse aquí mostrando el token
    else:
        form = SolicitudPedidoForm()

    return render(request, 'crear_pedido.html', {'form': form, 'token': token_generado})

def seguimiento(request):
    pedido = None
    if request.method == 'GET':
        token = request.GET.get('token')
        if token:
            try:
                pedido = Pedido.objects.get(token_seguimiento=token)
            except Pedido.DoesNotExist:
                messages.error(request, "No encontramos un pedido con ese código ")

    return render(request, 'seguimiento.html', {'pedido': pedido})