from django.contrib import admin
from .models import Categoria,Producto, ImagenProducto, Insumo, Pedido, ImagenPedido



#Apartado en admin para las categorías
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre_categoria", "descripcion_categoria")
    search_fields = ("nombre_categoria",)


#Apartado en Admin para que se muestren las imagenes
class ImagenProductoInline(admin.TabularInline):
    model = ImagenProducto
    extra = 1
    max_num = 3
    readonly_fields = ("orden",)


#Apartado en Admin para los Productos
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre_producto", "categoria_producto", "precio_base_producto", "producto_destacado")
    list_filter = ("categoria_producto", "producto_destacado")
    search_fields = ("nombre_producto", "descripcion_producto")
    inlines = [ImagenProductoInline]


#Apartado en Admin para los insumos
@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):
    list_display = ("nombre_insumo", "tipo_insumo", "marca_insumo", "color_insumo", "cantidad_disponible_insumo")
    search_fields = ("nombre_insumo", "tipo_insumo", "marca_insumo")
    list_filter = ("tipo_insumo", "marca_insumo")


#Para que se muestren ordenadas las imagenes de referencia de los pedidos
class ImagenPedidoInline(admin.TabularInline):
    model = ImagenPedido
    extra = 1
    max_num = 5
    readonly_fields = ("orden",)


#Apartado en Admin para los pedidos
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "cliente_nombre",
        "cliente_contacto",
        "producto",
        "estado_pedido",
        "estado_pago",
        "fecha_creacion",
    )
    list_filter = ("estado_pedido", "estado_pago", "origen_pedido")
    search_fields = ("cliente_nombre", "cliente_contacto", "descripcion")
    inlines = [ImagenPedidoInline]
    readonly_fields = ("token_seguimiento", "fecha_creacion")
    fieldsets = (
        ("Información del cliente", {
            "fields": ("cliente_nombre", "cliente_contacto")
        }),
        ("Detalles del pedido", {
            "fields": ("producto", "descripcion", "fecha_solicitada", "origen_pedido", "origen_otro", "producto_referencia")
        }),
        ("Estado y seguimiento", {
            "fields": ("estado_pedido", "estado_pago", "token_seguimiento", "fecha_creacion")
        }),
    )


#Clase para ver las imagenes de los pedidos de manera más ordenada
@admin.register(ImagenPedido)
class ImagenPedidoAdmin(admin.ModelAdmin):
    list_display = ("pedido", "imagen", "orden")
    list_filter = ("pedido",)
    readonly_fields = ("orden",)