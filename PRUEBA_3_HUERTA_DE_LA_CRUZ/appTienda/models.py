from django.contrib import admin
from .models import Categoria, Producto, Insumo, Pedido
from django.utils.html import format_html

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio_base', 'mostrar_imagen')
    list_filter = ('categoria', 'destacado')
    search_fields = ('nombre',)

    def mostrar_imagen(self, obj):
        if obj.imagen_principal:
            return format_html('<img src="{}" width="50" style="border-radius:10px;" />', obj.imagen_principal.url)
        return "Sin imagen"
    mostrar_imagen.short_description = "Vista Previa"

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente_nombre', 'estado_pedido', 'estado_pago', 'plataforma', 'fecha_entrega_deseada')
    list_filter = ('estado_pedido', 'estado_pago', 'plataforma')
    search_fields = ('cliente_nombre', 'token_seguimiento')
    readonly_fields = ('token_seguimiento', 'fecha_creacion') # Importante: No dejar editar el token

    #Organizar los campos por secciones
    fieldsets = (
        ('Información del Cliente', {
            'fields': ('cliente_nombre', 'contacto')
        }),
        ('Detalle del Pedido', {
            'fields': ('producto_referencia', 'descripcion_solicitud', 'imagen_referencia', 'fecha_entrega_deseada')
        }),
        ('Gestión Interna', {
            'fields': ('estado_pedido', 'estado_pago', 'plataforma')
        }),
        ('Sistema', {
            'fields': ('token_seguimiento', 'fecha_creacion'),
            'classes': ('collapse',)
        }),
    )

#Registros simples
admin.site.register(Categoria)
admin.site.register(Insumo)

