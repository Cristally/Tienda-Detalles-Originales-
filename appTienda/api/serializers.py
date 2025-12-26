from rest_framework import serializers
from appTienda.models import Categoria, Producto, ImagenProducto, Insumo, Pedido, ImagenPedido

class ImagenProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenProducto
        fields = ['id', 'imagen', 'orden']

class ProductoSerializer(serializers.ModelSerializer):
    imagenes = ImagenProductoSerializer(many=True, read_only=True)
    categoria_nombre = serializers.CharField(source='categoria_producto.nombre_categoria', read_only=True)
    view_name = "Listado de Productos"
    class Meta:
        model = Producto
        fields = ['id', 'nombre_producto', 'descripcion_producto', 'categoria_producto', 'categoria_nombre', 'precio_base_producto', 'producto_destacado', 'imagenes']





class ReportesDePedidos(serializers.Serializer):
    plataforma = serializers.CharField()
    total = serializers.IntegerField()




class CategoriaSerializer(serializers.ModelSerializer):
    productos = ProductoSerializer(many=True, read_only=True)

    class Meta:
        model = Categoria
        fields = ['id', 'nombre_categoria', 'descripcion_categoria', 'productos']

class InsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insumo
        fields = ['id', 'nombre_insumo', 'tipo_insumo', 'cantidad_disponible_insumo', 'marca_insumo', 'color_insumo']

class ImagenPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenPedido
        fields = ['id', 'imagen', 'orden']

class PedidoSerializer(serializers.ModelSerializer):
    imagenes = ImagenPedidoSerializer(many=True, read_only=True)
    producto_nombre = serializers.CharField(source='producto.nombre_producto', read_only=True, allow_null=True)

    class Meta:
        model = Pedido
        fields = ['id', 'cliente_nombre', 'cliente_contacto', 'producto', 'producto_nombre', 'descripcion', 'fecha_solicitada', 'origen_pedido', 'origen_otro', 'estado_pedido', 'estado_pago', 'token_seguimiento', 'fecha_creacion', 'producto_referencia', 'imagenes']