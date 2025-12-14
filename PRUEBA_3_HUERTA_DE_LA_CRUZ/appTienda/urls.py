from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.catalogo ),
    path('detalles/<int:id>', views.detalle, name="detalle"),
    path('pedido/', views.pedido)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
