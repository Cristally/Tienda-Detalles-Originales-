# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.Base )
# ]

from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .api import views as api_views
from django.contrib import messages
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView
)
from django.urls import path


@require_http_methods(["POST", "GET"])
def login_view(request):
    if request.user.is_authenticated:
        return redirect('catalogo')
    
    if request.method == 'POST':
        from django.contrib.auth import authenticate, login
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido {username}! Has iniciado sesión correctamente.')
            return redirect('catalogo')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    
    from django.contrib.auth.forms import AuthenticationForm
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('/')

from django.shortcuts import render

urlpatterns = [
    path('accounts/login/', login_view, name='login'),
    path('accounts/logout/', logout_view, name='logout'),

    path('', views.catalogo, name='home'),

    path('catalogo/', views.catalogo, name='catalogo'), 
    path('pedir/', views.crear_pedido, name='crear_pedido'),
    path('seguimiento/', views.seguimiento, name='seguimiento'),
    path('buscar-pedidos/', views.buscar_pedidos, name='buscar_pedidos'),
    path('insumos/', views.lista_insumos, name='lista_insumos'),
    path('pedido/boleta/<uuid:token>/', views.generar_pdf_token, name='generar_pdf_token'), #Para poder hacer los pdf con las boletas
    path('declaracion-ia/', views.generar_pdf_IA, name='declaracion-ia'), #Para la declaración de uso de IA
    path('producto/<int:producto_id>/', views.productos_detalles, name='productos_detalles'),
    path('api/', views.apihtml),
    path('api/pedidos_admin/', views.seguimiento_admin, name='api_seguimiento_admin'),
    path('api/reporte', api_views.apiReporte, name="apiReporte"),
    path('api/seguimiento/admin', api_views.pedidosAdmin, name='api_pedidos_admin'),

    #API Categorías
    path('api/categorias/crear/', api_views.CategoriaListCreateView.as_view(), name='api_categorias_create'),  #Crear Categorias
    path('api/categorias/', api_views.CategoriaListView.as_view(), name='api_categorias_list'),    #Listar Categorias
    path('api/categorias/<int:pk>/', api_views.CategoriaUpdateView.as_view(), name='api_categoria_update'), #Modificar Categoría
    path('api/categorias/<int:pk>/delete/', api_views.CategoriaDeleteView.as_view(), name='api_categoria_delete'),  #Eliminar Categoría


    #API Insumos
    path('api/opciones-insumos/', api_views.opcionesInsumos, name='api_opciones_insumos'),  #Página de opciones de insumos
    path('api/insumos/', api_views.InsumoListView.as_view(), name='api_insumos_list'),      #Ver insumos
    path('api/insumos/crear/', api_views.InsumoListCreateView.as_view(), name='api_insumos_create'),    #Añadir insumos
    path('api/insumos/<int:pk>/', api_views.InsumoDetailUpdateView.as_view(), name='api_insumo_detail_update'), #Ver y Actualizar insumo específico
    path('api/insumos/<int:pk>/delete/', api_views.InsumoDeleteView.as_view(), name='api_insumo_delete'), #Eliminar Insumos
    path('api/insumos/filtrar/<str:nombre>/', api_views.InsumoNombreView.as_view(), name='api_insumo_nombre'), #Ver insumo especifico por nombre


    #API Productos
    path('api/productos/crear/', api_views.ProductoListCreateView.as_view(), name='api_productos_create'),
    path('api/productos/', api_views.ProductoListCreateView.as_view(), name='api_productos_list_create'),
    path('api/productos/<int:pk>/', api_views.ProductoUpdateView.as_view(), name='api_producto_update'),
    path('api/productos/<int:pk>/delete/', api_views.ProductoDeleteView.as_view(), name='api_producto_delete'),



    #API Pedidos
    path('api/pedidos/crear/', api_views.PedidoCreateView.as_view(), name='api_pedidos_create'),
    path('api/pedidos/<int:pk>/', api_views.PedidoUpdateView.as_view(), name='api_pedido_update'),
    path('api/pedidos/filtrar/<uuid:token>/', api_views.PedidoTokenView.as_view(), name='api_pedido_token'),
    path('api/pedidos/filtrar/estado/<str:estado_pedido>/', api_views.PedidoEstadoView.as_view(), name='api_pedido_estado'),
    path('api/pedidos/filtrar/estado_pago/<str:estado_pago>/', api_views.PedidoPagoView.as_view(), name='api_pedido_estado_pago'),
    path('api/pedidos/filtrar/por-fecha/', api_views.PedidoFechaView.as_view(), name='api_pedidos_por_fecha'),
    #Extras
    path('api/reporte_reporte', api_views.apiReporteSeri, name='apiReporteSeri'),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema')),
]

#Para poder ver imagenes
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)