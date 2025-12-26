from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework import generics, mixins
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Sum, Case, When, F, Count, CharField
from appTienda.models import Categoria, Producto, Insumo, Pedido
from .serializers import CategoriaSerializer, ProductoSerializer, InsumoSerializer, PedidoSerializer, ReportesDePedidos
from .permissions import IsAdminUser
import requests
from rest_framework.test import APIRequestFactory
from rest_framework import status
from django.http import HttpResponse
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime
import random
from rest_framework.request import Request


@login_required
def apiReporte(request):
    
    return render(request, 'api_reporte.html')

@api_view(["GET"])
def apiReporteSeri(request):
    queryset = (
        Pedido.objects
        .annotate(
            plataforma=Case(
                When(origen_pedido="OTR", then=F("origen_otro")),
                default=F("origen_pedido"),
                output_field=CharField()
            )
        )
        .values("plataforma")
        .annotate(total=Count("id"))
        .order_by("plataforma")
    )

    serializer = ReportesDePedidos(queryset, many=True)
    return Response(serializer.data)


# Vista para el reporte


@login_required
def opcionesInsumos(request):
    return render(request, "insumo.html")

@login_required
def pedidosAdmin(request):
    return render(request, "seguimientoadmin.html")

##################################################################################
##################################################################################
##################################################################################

#Categorías
#Añadir Categorías
class CategoriaListCreateView(generics.ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAdminUser]

    def get_view_name(self):
        return "Añadir Nueva Categoría"

#Ver Categorías
class CategoriaListView(generics.ListAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAdminUser]
    def get_view_name(self):
        return "Listado de Categorías"
    



#Actualizar categorias
class CategoriaUpdateView(generics.UpdateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAdminUser]
    def get_view_name(self):
        try:
            categoria = self.get_object()
            return f"Actualizar Datos de Categoría: {categoria.nombre_categoria}"
        
        except Exception:
            return "Actualizar Categoría"


#Eliminar categorias
class CategoriaDeleteView(generics.DestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAdminUser]
    def get_view_name(self):
        try:
            categoria = self.get_object()
            return f"Eliminar Datos de Categoría: {categoria.nombre_categoria}"
        
        except Exception:
            return "Eliminar Categoría"
##################################################################################
##################################################################################
##################################################################################


#Insumos
#Añadir insumos
class InsumoListCreateView(generics.ListCreateAPIView):
    queryset = Insumo.objects.all()
    serializer_class = InsumoSerializer
    permission_classes = [IsAdminUser]

    def get_view_name(self):
        return "Añadir Nuevo Insumo"

#Ver insumos
class InsumoListView(generics.ListAPIView):
    queryset = Insumo.objects.all()
    serializer_class = InsumoSerializer
    permission_classes = [IsAdminUser]
    def get_view_name(self):
        return "Listado de Insumos"

#Ver y Actualizar insumo específico
class InsumoDetailUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Insumo.objects.all()
    serializer_class = InsumoSerializer
    permission_classes = [IsAdminUser]
    def get_view_name(self):
        try:
            insumo = self.get_object()
            return f"Detalles y Actualizar Insumo: {insumo.nombre_insumo}"
        except Exception:
            return "Detalles del Insumo"

#Actualizar insumos
class InsumoUpdateView(generics.UpdateAPIView):
    queryset = Insumo.objects.all()
    serializer_class = InsumoSerializer
    permission_classes = [IsAdminUser]
    def get_view_name(self):
        try:
            insumo = self.get_object()
            return f"Actualizar Datos del Insumo: {insumo.nombre_insumo}"
        
        except Exception:
            return "Actualizar Insumo"
        

#Ver Insumo Especifico
class InsumoNombreView(generics.RetrieveAPIView):
    queryset = Insumo.objects.all()
    serializer_class = InsumoSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'nombre_insumo'
    lookup_url_kwarg = 'nombre'

#Eliminar Insumos
class InsumoDeleteView(generics.DestroyAPIView):
    queryset = Insumo.objects.all()
    serializer_class = InsumoSerializer
    permission_classes = [IsAdminUser]
    def get_view_name(self):
        try:
            insumo = self.get_object()
            return f"Eliminar Datos del Insumo: {insumo.nombre_insumo}"
        
        except Exception:
            return "Eliminar Insumo"
##################################################################################
##################################################################################
##################################################################################





#Productos
#Añadir
class ProductoListCreateView(generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAdminUser]

    def get_view_name(self):
        return "Añadir Producto"


#Ver productos
class ProductoListView(generics.ListAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAdminUser]

    def get_view_name(self):
        return "Listado de Productos"


#Actualizar productos
class ProductoUpdateView(generics.UpdateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAdminUser]

    def get_view_name(self):
        try:
            producto = self.get_object()
            return f"Actualizar Datos del Producto: {producto.nombre_producto}"
        
        except Exception:
            return "Actualizar Producto"


#Eliminar productos
class ProductoDeleteView(generics.DestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAdminUser]

    def get_view_name(self):
        try:
            producto = self.get_object()
            return f"Eliminar Datos del Producto: {producto.nombre_producto}"
        
        except Exception:
            return "Eliminar Producto"
        
##################################################################################
##################################################################################
##################################################################################

#Pedido
#Añadir Pedidos
class PedidoCreateView(generics.CreateAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [IsAdminUser]
    def get_view_name(self):
        return "Crear Nuevo Pedido"

#Actualizar pedidos
class PedidoUpdateView(generics.UpdateAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [IsAdminUser]
    def get_view_name(self):
        return "Actualizar datos de Pedido"

#Ver pedidos por token
class PedidoTokenView(generics.RetrieveAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'token_seguimiento'
    lookup_url_kwarg = 'token'
    

#Ver Pedidos por Estado
class PedidoEstadoView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Pedido.objects.all()
        estado = self.kwargs.get('estado_pedido') or self.request.query_params.get('estado_pedido')
        if estado:
            queryset = queryset.filter(estado_pedido=estado)
        limit = self.request.query_params.get('limit')
        try:
            if limit:
                limit_i = int(limit)
                if limit_i > 0:
                    queryset = queryset[:limit_i]
        except Exception:
            pass
        return queryset


#Ver Pedidos por Estado de Pago
class PedidoPagoView(generics.ListAPIView):
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Pedido.objects.all()
        estado_pago = self.kwargs.get('estado_pago') or self.request.query_params.get('estado_pago')
        if estado_pago:
            queryset = queryset.filter(estado_pago=estado_pago)
        limit = self.request.query_params.get('limit')
        try:
            if limit:
                limit_i = int(limit)
                if limit_i > 0:
                    queryset = queryset[:limit_i]
        except Exception:
            pass
        return queryset


#Ver Pedidos por Fecha en la que fueron solicitados
class PedidoFechaView(generics.ListAPIView):
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset = Pedido.objects.all()
        fecha_desde = self.request.query_params.get('desde')
        fecha_hasta = self.request.query_params.get('hasta')

        if fecha_desde and fecha_hasta:
            queryset = queryset.filter(
                fecha_solicitada__range=[fecha_desde, fecha_hasta]
            )
        limit = self.request.query_params.get('limit')
        try:
            if limit:
                limit_i = int(limit)
                if limit_i > 0:
                    queryset = queryset[:limit_i]
        except Exception:
            pass

        return queryset


#Eliminar productos
#class PedidoDeleteView(generics.DestroyAPIView):
#    queryset = Pedido.objects.all()
#    serializer_class = PedidoSerializer




#Extras
#Reporte PDF de un pedido
class pedidoPDFView(APIView):
    def get(self, request, token):
        api_url = request.build_absolute_uri(f'/api/pedido/filtrar/{token}/')
        try:
            response = requests.get(api_url)

            if response.status_code != 200:
                return Response({"error": "Pedido no encontrado"}, status=status.HTTP_404_NOT_FOUND)
            pedido_data = response.json()

        except requests.exceptions.RequestException:
            return Response({"error": "Error al obtener datos del pedido"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='CenterTitle', alignment=1, fontSize=16, spaceAfter=20))

        elements.append(Paragraph(f"Boleta de Pedido #{pedido_data['id']}", styles['CenterTitle']))

        cliente_info = [
            ['Cliente:', pedido_data['cliente_nombre']],
            ['Contacto:', pedido_data['cliente_contacto']],
            ['Fecha de Solicitud:', pedido_data.get('fecha_solicitada', 'No especificada')],
            ['Origen del Pedido:', pedido_data.get('origen_pedido', 'No especificado')],
            ['Estado del Pedido:', pedido_data.get('estado_pedido', 'No especificado')],
            ['Estado del Pago:', pedido_data.get('estado_pago', 'No especificado')],
            ['Token de Seguimiento:', str(pedido_data['token_seguimiento'])],
        ]

        table_cliente = Table(cliente_info, colWidths=[150, 350])
        table_cliente.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            ('ALIGN',(0,0),(-1,-1),'LEFT'),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ]))
        elements.append(table_cliente)
        elements.append(Spacer(1, 20))

        producto = pedido_data.get('producto')
        if producto:
            producto_info = [
                ['Producto', 'Categoría', 'Precio', 'Descripción'],
                [
                    producto['nombre_producto'],
                    producto['categoria_producto']['nombre_categoria'],
                    f"${random.randint(5990, 49990) + producto['precio_base_producto']}",
                    producto.get('descripcion_producto', '')
                ]
            ]
            table_producto = Table(producto_info, colWidths=[120, 120, 80, 180])
            table_producto.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
                ('ALIGN',(0,0),(-1,-1),'LEFT'),
                ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
                ('FONTSIZE', (0,0), (-1,-1), 10),
                ('BOTTOMPADDING', (0,0), (-1,-1), 6),
                ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ]))
            elements.append(Paragraph("Información del Producto", styles['Heading3']))
            elements.append(table_producto)
            elements.append(Spacer(1, 20))

        if pedido_data.get('descripcion'):
            elements.append(Paragraph("Descripción del Pedido:", styles['Heading3']))
            elements.append(Paragraph(pedido_data['descripcion'], styles['Normal']))

        doc.build(elements)
        buffer.seek(0)

        fecha_actual = datetime.now().strftime('%d%m%Y_%H%M%S')
        response_pdf = HttpResponse(buffer, content_type='application/pdf')
        response_pdf['Content-Disposition'] = f'inline; filename="Boleta_Pedido_{pedido_data["id"]}_{fecha_actual}.pdf"'
        return response_pdf

