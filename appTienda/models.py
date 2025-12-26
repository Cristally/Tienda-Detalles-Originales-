#Importaciones
import uuid     #UUID para generar los tokens de seguimiento
from django.db import models        #Importación basica para hacer los models
from django.core.exceptions import ValidationError      #Importación para poder hacer ValidationError y limitar la cantidad de imagenes
from colorfield.fields import ColorField #Para poder tener una selección de color en los insumos (El fin es más que nada estetico)

#Clase para las categorias 
class Categoria(models.Model):
    nombre_categoria = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Categoría") 
    #Tamaño maximo de 100 caracteres
    #El nombre será unico
    #En el apartado de admin saldrá ese nombre (Verbose_name), en vez del nombre de la variable

    descripcion_categoria = models.TextField(blank=True)    #TextField para que no tenga max length

    class Meta:
        verbose_name = "Categoría"          #El nombre que tomará la clase en el admin 
        verbose_name_plural = "Categorías"      #El nombre que tomará la clase en el admin, en plural

    def __str__(self):
        return self.nombre_categoria




#Productos en tienda
class Producto(models.Model):
    nombre_producto = models.CharField(max_length=100, verbose_name="Nombre del Producto")
    descripcion_producto = models.TextField(verbose_name="Descripción del producto")
    categoria_producto = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="productos", verbose_name="Categoria del producto")
    precio_base_producto = models.PositiveIntegerField(verbose_name="Precio del Producto")
    #PositiveIntegerField para que sean SOLO números enteros y positivos (Así no sale 24990.0 o -12990)

    producto_destacado = models.BooleanField(default=False, verbose_name="Producto Destacado Sí/No")
    #Boolean para marcar los productos destacados 


    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.nombre_producto


#Clase para las imagenes de los productos
class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="imagenes")
    imagen = models.ImageField(upload_to="productos/")
    orden = models.PositiveSmallIntegerField(default=0)
        #Metodo para comprobar que las imagenes no sean más de 3
    #Se envia un ValidationError si se intenta subir una 4 imagen
    def clean(self):
        if self.producto and self.producto.pk:
            if self.producto.imagenes.count() >= 3 and not self.pk:
                raise ValidationError("Un producto no puede tener más de 3 imágenes.")

    class Meta:
        verbose_name = "Imagen de producto"
        verbose_name_plural = "Imágenes de productos"
        ordering = ["orden"]        #El como se ordenarán las imagenes



        

#Clase para los insumos
class Insumo(models.Model):
    nombre_insumo = models.CharField(max_length=100, verbose_name="Nombre del Insumo")
    tipo_insumo = models.CharField(max_length=100, verbose_name="Tipo de Insumo")
    cantidad_disponible_insumo = models.PositiveIntegerField(verbose_name="Cantidad Disponible del Insumo")
    marca_insumo = models.CharField(max_length=50, verbose_name="Marca del Insumo")
    color_insumo = ColorField(default="#FFFFFF")

    class Meta:
        verbose_name = "Insumo"
        verbose_name_plural = "Insumos"

    def __str__(self):
        return f"{self.nombre_insumo} ({self.cantidad_disponible_insumo})"
    

#Clase para los pedidos
class Pedido(models.Model):
    #Clase para las opciones
    class Origen(models.TextChoices):
        facebook = "FAC", "Facebook"
        instagram = "IG", "Instagram"
        whatsapp = "WHA", "WhatsApp"
        presencial = "PRE", "Presencial"
        web = "WEB", "Sitio Web"
        otro = "OTR", "Otro"
        #El como se almacenará en la base de datos, a la derecha el valor que representa. IG = Instagram


    class EstadoPedido(models.TextChoices):
        solicitado = "SOL", "Solicitado"
        aprobado = "APR", "Aprobado"
        en_proceso = "EPR", "En proceso"
        realizado = "REA", "Realizado"
        entregado = "ENT", "Entregado"
        finalizado = "FIN", "Finalizado"
        cancelado = "CAN", "Cancelado"


    class EstadoPago(models.TextChoices):
        pendiente = "PEN", "Pendiente"
        parcial = "PAR", "Parcial"
        pagado = "PAG", "Pagado"
        reembolsado = "REM", "Reembolsado"      #No se especifica en la rubrica, pero es un estado que consideramos importante



    cliente_nombre = models.CharField(max_length=100, verbose_name="Nombre del cliente")
    cliente_contacto = models.CharField(max_length=100, verbose_name="Contacto del cliente")
    producto = models.ForeignKey(Producto,null=True, blank=True,on_delete=models.SET_NULL,related_name="pedidos")
    descripcion = models.TextField(verbose_name="Descripción")
    fecha_solicitada = models.DateField(null=True, blank=True, verbose_name="Fecha Solicitada del Pedido")
    origen_pedido = models.CharField(max_length=10, choices=Origen.choices, verbose_name="Origen del Pedido")
    origen_otro = models.CharField(max_length=100, blank=True, verbose_name="Origen (Otro)")
    estado_pedido = models.CharField(max_length=3,choices=EstadoPedido.choices,default=EstadoPedido.solicitado, verbose_name="Estado del Pedido")
    estado_pago = models.CharField(max_length=3,choices=EstadoPago.choices,default=EstadoPago.pendiente, verbose_name="Estado del Pago")
    token_seguimiento = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, verbose_name="Token de Seguimiento")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación del Pedido")
    producto_referencia = models.ImageField(
    upload_to="pedidos/referencias/",
    null=True,
    blank=True,
    verbose_name="Imagen de referencia"
    )
    #Metodo para evitar establecer el estado del pedido como finalizado si el estado de pago no es "Pagado"
    def clean(self):
        # Validación de estado finalizado - solo si el objeto ya existe
        if self.pk:
            if self.estado_pedido == self.EstadoPedido.finalizado and self.estado_pago != self.EstadoPago.pagado:
                raise ValidationError("No se puede finalizar un pedido que no esté pagado.")

            # Validación de imágenes: solo si el objeto ya existe
            if self.imagenes.count() > 5:
                raise ValidationError("No se puede añadir más de 5 imágenes a este pedido.")
            
    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente_nombre}"
    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"


class Usuario(models.Model):
    usuario = models.CharField(max_length=100, verbose_name="Nombre de Usuario")
    contrasena = models.CharField(max_length=100, verbose_name="Contraseña")
    rol = models.CharField(max_length=50, verbose_name="Rol del Usuario")
    


#Clase para gestionar las imagenes de referencia de los pedidos. No pueden ser más de 5
class ImagenPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="imagenes", verbose_name="Pedido")
    imagen = models.ImageField(upload_to="pedidos/referencias/", verbose_name="Imagenes de Referencia")
    orden = models.PositiveSmallIntegerField(default=0)

    def clean(self):
        if self.pedido and self.pedido.pk:
            if self.pedido.imagenes.count() >= 5 and not self.pk:
                raise ValidationError("Un pedido no puede tener más de 5 imágenes de referencia.")

    class Meta:
        verbose_name = "Imagen de pedido"
        verbose_name_plural = "Imágenes de pedidos"
        ordering = ["orden"]

        
