import uuid
from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    precio_base = models.DecimalField(max_digits=10, decimal_places=0)
    imagen_principal = models.ImageField(upload_to='productos/')
    # Opcional: Podrías agregar más imágenes si usas un modelo relacionado, 
    # pero por simplicidad dejaremos una principal aquí.
    destacado = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

class Insumo(models.Model):
    UNIDADES = [('un', 'Unidad'), ('gr', 'Gramos'), ('mt', 'Metros')]
    
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    unidad = models.CharField(max_length=5, choices=UNIDADES, default='un')
    marca = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.cantidad} {self.unidad})"

class Pedido(models.Model):
    ESTADOS_PEDIDO = [
        ('solicitado', 'Solicitado 📩'),
        ('aprobado', 'Aprobado ✅'),
        ('proceso', 'En Proceso 🎨'),
        ('realizada', 'Realizada 🛠'),
        ('entregada', 'Entregada 📦'),
        ('finalizada', 'Finalizada ✨'),
        ('cancelada', 'Cancelada ❌'),
    ]
    
    PLATAFORMAS = [
        ('web', 'Sitio Web'),
        ('fb', 'Facebook'),
        ('ig', 'Instagram'),
        ('wpp', 'WhatsApp'),
        ('presencial', 'Presencial'),
    ]

    PAGO_ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('parcial', 'Parcial'),
        ('pagado', 'Pagado'),
    ]

    # Datos del Cliente
    cliente_nombre = models.CharField(max_length=200)
    contacto = models.CharField(max_length=200, help_text="Email, Teléfono o Usuario RRSS")
    
    # Datos del Pedido
    producto_referencia = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=True)
    descripcion_solicitud = models.TextField()
    imagen_referencia = models.ImageField(upload_to='referencias_clientes/', blank=True, null=True)
    fecha_entrega_deseada = models.DateField(null=True, blank=True)
    
    # Gestión Interna
    plataforma = models.CharField(max_length=20, choices=PLATAFORMAS, default='web')
    estado_pedido = models.CharField(max_length=20, choices=ESTADOS_PEDIDO, default='solicitado')
    estado_pago = models.CharField(max_length=20, choices=PAGO_ESTADOS, default='pendiente')
    
    # El Token Mágico
    token_seguimiento = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente_nombre}"
