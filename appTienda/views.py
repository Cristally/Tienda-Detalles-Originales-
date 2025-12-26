from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Pedido, Categoria, Insumo
from .forms import SolicitudPedidoForm
from django.contrib import messages
from django.db.models import Q # Para el buscador
from django.contrib.auth.decorators import user_passes_test, login_required #Para hacer apartados solo para admins
from django.http import JsonResponse
from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from datetime import datetime
import random

#Views para el catalogo
def catalogo(request):
    productos = Producto.objects.all()  #Toma todos los productos
    categorias = Categoria.objects.all() #Toma todas las categorias
    return render(request, 'catalogo.html', {
        'productos': productos,
        'categoria': categorias
    })      #Envia estos archivos al apartado del catalogo, para que se muestren


def productos_detalles(request, producto_id):
    # Buscamos el producto específico por su ID o devolvemos error 404 si no existe
    producto = get_object_or_404(Producto, id=producto_id)
    
    # Renderizamos la plantilla enviando ese único producto
    return render(request, 'productos.html', {
        'producto': producto})


#Views para crear el pedido
def crear_pedido(request):
    token_generado = None
    

    producto_id = request.GET.get('ref')
    producto_seleccionado = None
    if producto_id:
        producto_seleccionado = Producto.objects.filter(id=producto_id).first()

    if request.method == 'POST':
        form = SolicitudPedidoForm(request.POST, request.FILES)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.origen_pedido = 'WEB'  # Siempre desde sitio web
            pedido.estado_pedido = 'SOL'  # Usar el código correcto
            pedido.estado_pago = 'PEN'    # Usar el código correcto
            
            pedido.save()
            
            # Procesar imágenes múltiples
            imagenes = request.FILES.getlist('imagenes')
            for idx, imagen in enumerate(imagenes):
                from .models import ImagenPedido
                ImagenPedido.objects.create(
                    pedido=pedido,
                    imagen=imagen,
                    orden=idx
                )
            
            token_generado = pedido.token_seguimiento #Se genera una vez el pedido se guarda (Es valido)
            messages.success(request, f'¡Pedido recibido! Tu token es: {token_generado}')

            
    else:
        initial_data = {'origen_pedido': 'WEB'}
        if producto_seleccionado:
            initial_data['producto'] = producto_seleccionado
        form = SolicitudPedidoForm(initial=initial_data)
    
    return render(request, 'crear_pedido.html', {
        'form': form, 
        'token': token_generado,
        'producto_preseleccionado': producto_seleccionado,
        'tiene_producto': bool(producto_seleccionado)
    })


#Seguimiento mediante el token
def seguimiento(request):
    pedido = None
    if request.method == 'GET':
        token = request.GET.get('token')
        if token:
            try:
                pedido = Pedido.objects.get(token_seguimiento=token)
            except Pedido.DoesNotExist:
                messages.error(request, "Token no válido.")
    return render(request, 'seguimiento.html', {'pedido': pedido})




#Para los insumos
@user_passes_test(lambda u: u.is_staff, login_url='/admin/login/')  #Requiere que el usuario ingrese como admin
#Al no estar ingresado, redirigira al usuario a admin/login/, del propio django
def lista_insumos(request):
    insumos = Insumo.objects.all()
    return render(request, 'insumos.html', {'insumos': insumos})






#Para poder generar los pdf en base al token
def generar_pdf_token(request, token):
    try:
        pedido = Pedido.objects.get(token_seguimiento=token) #Buscar el pedido por token en 
    except Pedido.DoesNotExist:
        return HttpResponse("Pedido no encontrado", status=404)     #En caso de que no se encuentre el pedido, generará error 404

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []       #Apartado del modulo de pdf para generar el documento



    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='CenterTitle', alignment=1, fontSize=16, spaceAfter=20))
    #Estilos del pdf para el titulo

    #Título del pdf dentro del documento
    elements.append(Paragraph(f"Boleta de Pedido #{pedido.id}", styles['CenterTitle']))

    #Toda la información del cliente
    cliente_info = [
        ['Cliente:', pedido.cliente_nombre],
        ['Contacto:', pedido.cliente_contacto],
        ['Fecha de Solicitud:', pedido.fecha_solicitada.strftime('%d/%m/%Y') if pedido.fecha_solicitada else 'No especificada'],
        #Al ser opcional la fecha, en caso de no haber, se pone que no fue especificada
        ['Origen del Pedido:', pedido.get_origen_pedido_display()],
        ['Estado del Pedido:', pedido.get_estado_pedido_display()],
        ['Estado del Pago:', pedido.get_estado_pago_display()],
        ['Token de Seguimiento:', str(pedido.token_seguimiento)],
    ]

    #Tabla con toda la información de las lineas anteriores
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

    #Información del producto
    if pedido.producto:
        producto_info = [
            ['Producto', 'Categoría', 'Precio', 'Descripción'],
            [
                pedido.producto.nombre_producto,
                pedido.producto.categoria_producto.nombre_categoria,
                 f"${random.randint(5990, 49990) + pedido.producto.precio_base_producto}", 
                 #Para no poseer confusiones con el precio del producto en si, 
                 #se toma el valor del producto y se suma por un número aleatorio, para simular valores

                pedido.producto.descripcion_producto
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




    if pedido.descripcion:
        elements.append(Paragraph("Descripción del Pedido:", styles['Heading3']))
        elements.append(Paragraph(pedido.descripcion, styles['Normal']))

    doc.build(elements)
    buffer.seek(0)

    fecha_actual = datetime.now().strftime('%d%m%Y_%H%M%S')
    response = HttpResponse(buffer, content_type='application/pdf') #Para que el navegador muestre la información como archivo pdf y no como página web
    response['Content-Disposition'] = f'inline; filename="Boleta_Pedido_{pedido.id}_{fecha_actual}.pdf"' #Nombre que recibe el archivo
    return response




def generar_pdf_IA(request):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    #stilos
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='CenterTitle', alignment=1, fontSize=16, spaceAfter=20))
    styles.add(ParagraphStyle(name='TableBody', fontName='Helvetica', fontSize=9, leading=11))

    #Título
    elements.append(Paragraph("Declaración de Uso de Inteligencia Artificial", styles['CenterTitle']))
    elements.append(Spacer(1, 12))

    #Encabezado
    data = [[
        'Archivo', 'Porcentaje utilizando IA', 'Herramienta Utilizada', 'Ayuda Extra', 'Descripción'
    ]]


    registros = [
        {
            'archivo': 'views.py',
            'porcentaje': '5%',
            'herramienta': 'ChatGPT',
            'ayuda': 'Depuración',
            'descripcion': 'Pruebas y busqueda de errores'
        },
        {
            'archivo': 'admin.py',
            'porcentaje': '10%',
            'herramienta': 'ChatGPT',
            'ayuda': 'Ayuda',
            'descripcion': 'Ayuda con lo relacionado con el manejo de las imagenes'
        },
        {
            'archivo': 'forms.py',
            'porcentaje': '10%',
            'herramienta': 'ChatGPT',
            'ayuda': 'Depuración',
            'descripcion': 'Busqueda y (A veces) corrección de errores'
        },
        {
            'archivo': 'models.py',
            'porcentaje': '2%',
            'herramienta': 'ChatGPT',
            'ayuda': 'Imagenes',
            'descripcion': 'Ayuda con ideas para hacer lo de las multiples imagenes'
        },
        {
            'archivo': 'urls.py',
            'porcentaje': '0%',
            'herramienta': '---',
            'ayuda': '---',
            'descripcion': '---'
        },
        {
            'archivo': 'settings.py',
            'porcentaje': '0%',
            'herramienta': '---',
            'ayuda': '---',
            'descripcion': '---'
        },
        {
            'archivo': 'models.py',
            'porcentaje': '2%',
            'herramienta': 'ChatGPT',
            'ayuda': 'Imagenes',
            'descripcion': 'Ayuda con ideas para hacer lo de las multiples imagenes'
        },
        {
            'archivo': 'models.py',
            'porcentaje': '2%',
            'herramienta': 'ChatGPT',
            'ayuda': 'Imagenes',
            'descripcion': 'Ayuda con ideas para hacer lo de las multiples imagenes'
        },
        {
            'archivo': 'crear_pedido.html',
            'porcentaje': 1,
            'herramienta': '-',
            'ayuda': '',
            'descripcion': 'Ayuda con ideas para hacer lo de las multiples imagenes'
        },
        {
            'archivo': 'insumos.html',
            'porcentaje': 0,
            'herramienta': '-',
            'ayuda': '-',
            'descripcion': '-'
        },
        {
            'archivo': 'productos.html',
            'porcentaje': 2,
            'herramienta': 'Gemini',
            'ayuda': 'Solución de Errores',
            'descripcion': 'Solución para errores de Bootstrap'
        },
        {
            'archivo': 'seguimiento.html',
            'porcentaje': 8,
            'herramienta': 'ChatGPT',
            'ayuda': 'Diseño',
            'descripcion': 'Ayuda con el diseño del timeline'
        },
    ]

    # Agregar registros a la tabla
    for r in registros:
        data.append([
            Paragraph(r['archivo'], styles['TableBody']),
            Paragraph(f"{r['porcentaje']} %", styles['TableBody']),
            Paragraph(r['herramienta'], styles['TableBody']),
            Paragraph(r['ayuda'], styles['TableBody']),
            Paragraph(r['descripcion'], styles['TableBody']),
        ])

    # Crear tabla
    table = Table(data, colWidths=[120, 90, 100, 110, 170])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('ALIGN',(0,0),(-1,-1),'LEFT'),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ]))

    elements.append(table)

    # Construir PDF
    doc.build(elements)
    buffer.seek(0)

    # Respuesta HTTP
    fecha_actual = datetime.now().strftime('%d%m%Y_%H%M%S')
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="Declaracion_IA_{fecha_actual}.pdf"'
    return response

def apihtml(request):
    return render(request, 'api.html')


@user_passes_test(lambda u: u.is_staff, login_url='/admin/login/')
def seguimiento_admin(request):
    """Vista que muestra la plantilla de seguimiento para admin dentro del apartado API.

    Accesible solo para usuarios `is_staff`.
    """
    return render(request, 'seguimientoadmin.html')


@login_required
def buscar_pedidos(request):
    """Renderiza la página de búsqueda de pedidos (templates/buscar_pedidos.html).

    Accesible solo para usuarios autenticados.
    """
    return render(request, 'buscar_pedidos.html')