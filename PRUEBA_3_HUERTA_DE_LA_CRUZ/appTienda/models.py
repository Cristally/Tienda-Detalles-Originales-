from django.db import models

# Create your models here.
class Categoria():
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre
    
class Productos():
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField()
    precio_base = models.IntegerField()
    categoria = models.CharField(max_length=50, unique=True)
    imagen_producto1 = models.ImageField()
    imagen_producto2 = models.ImageField()
    imagen_producto3 = models.ImageField()

    def __str__(self):
        return self.nombre
    
class Insumos():
    nombre = models.CharField(max_length=50, unique=True)
    tipo = models.CharField(max_length=50, unique=True)
    cantidad = models.IntegerField()
    disponible = models.CharField(max_length=50, unique=True)
    unidad = models.CharField(max_length=50)
    marca = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=50, unique=True)
