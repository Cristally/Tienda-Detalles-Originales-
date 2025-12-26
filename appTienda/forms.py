from django import forms
from .models import Pedido, ImagenPedido, Usuario


#Formulario para los pedidos
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            "usuario",
            "contrasena",
            "rol"
        ]
        labels = {
            "usuario": "Nombre de Usuario",
            "contrasena": "Contraseña",
            "rol": "Rol del Usuario"
        }
        widgets = {
            "usuario": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nombre de Usuario",
                "required": True}),
            "contrasena": forms.PasswordInput(attrs={
                "class": "form-control",
                "placeholder": "Contraseña",
                "required": True}),
            "rol": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Rol del Usuario",
                "required": True}),
        }
    

class SolicitudPedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = [
            "cliente_nombre",
            "cliente_contacto",
            "producto",
            "descripcion",
            "fecha_solicitada",
            "producto_referencia"]      #Campos que posee la tabla de Pedidos


        labels = {
            "cliente_nombre": "Nombre del cliente",
            "cliente_contacto": "Contacto",
            "producto": "Producto a personalizar",
            "descripcion": "Descripción del pedido",
            "fecha_solicitada": "Fecha solicitada",
        }      
        

        widgets = {         #Para que se ponga en el html y se despliegue este tipo de formulario
            "cliente_nombre": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nombre completo",
                "required": True}),

            "cliente_contacto": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Teléfono o correo",
                "required": True}),

            "producto": forms.Select(attrs={
                "class": "form-control"}),

            "descripcion": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Describe el pedido (colores, talla, texto, etc.)",
                "required": True}),

            "fecha_solicitada": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control"}),

            "producto_referencia": forms.FileInput(attrs={
                "class": "form-control",
                "accept": "image/*"}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer producto no requerido por defecto (se requerirá solo si no viene del catálogo)
        self.fields['producto'].required = False



#Formulario para las imagenes en los pedidos
class ImagenPedidoForm(forms.ModelForm):
    class Meta:
        model = ImagenPedido
        fields = ["imagen"]

        widgets = {
            "imagen": forms.ClearableFileInput(attrs={
                "class": "form-control",
                "accept": "image/*"
            })
        }
