from django import forms
from .models import Pedido

class SolicitudPedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = [
            'cliente_nombre', 
            'contacto', 
            'producto_referencia', 
            'imagen_referencia', 
            'descripcion_solicitud', 
            'fecha_entrega_deseada'
            ]
        widgets = {
            'cliente_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'contacto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email, Teléfono o Usuario RRSS'}),
            'producto_referencia': forms.TextInput(attrs={'class': 'form-control'}),

            'descripcion_solicitud': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'fecha_entrega_deseada': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }