# 🎁 Tienda Detalles Originales

> Sistema web integral para la gestión de pedidos personalizados y control de inventario, desarrollado con Django.

![Status](https://img.shields.io/badge/Estado-En_Desarrollo-yellow)
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.0-green.svg)
![Style](https://img.shields.io/badge/Style-Cute%20Pastel-pink)

## 📖 Descripción del Proyecto

**Tienda Detalles Originales** es una solución web diseñada para optimizar el flujo de trabajo de una tienda de artículos personalizados (poleras, tazones, impresiones 3D). 

El sistema resuelve la problemática de la dispersión de pedidos (que llegan por WhatsApp, Instagram, presencial, etc.) centralizando todo en un único panel de administración, permitiendo además a los clientes solicitar productos vía web y realizar un seguimiento en tiempo real.

Este proyecto fue desarrollado como parte de la evaluación de la asignatura [Nombre de tu Asignatura] en un plazo de 2 semanas.

## ✨ Características Principales

### 🛍️ Vistas Públicas (Cliente)
* **Catálogo Visual:** Galería de productos filtrable por categorías (Ropa, Hogar, 3D).
* **Solicitud Personalizada:** Formulario amigable para subir imágenes de referencia y pedir cotizaciones.
* **Seguimiento de Pedidos:** Sistema de *Tracking* mediante Token único, donde el cliente ve el avance de su pedido en una línea de tiempo visual.

### 🛠️ Panel de Administración (Interno)
* **Gestión Centralizada:** Registro de pedidos provenientes de múltiples canales (Facebook, Web, Presencial).
* **Control de Inventario:** Gestión de insumos (stock de poleras, filamento, etc.) desconectado de ventas automáticas para control manual preciso.
* **Flujo de Estados:** Control estricto del ciclo de vida del pedido (Solicitado → Aprobado → En Proceso → Entregado).
* **Validaciones:** Reglas de negocio (ej. no finalizar pedidos sin pago completo).

## 🎨 Galería de Vistas
*(Aquí puedes subir tus capturas de pantalla a la carpeta /screenshots y enlazarlas)*

| Catálogo Público | Seguimiento de Pedido |
|:---:|:---:|
| ![Catalogo](ruta/a/tu/imagen_catalogo.png) | ![Tracking](ruta/a/tu/imagen_tracking.png) |

## 🚀 Tecnologías Utilizadas

* **Backend:** Python, Django Framework (Models, Views, Forms, Admin).
* **Frontend:** HTML5, CSS3 (Estilo "Cute/Pastel"), Bootstrap 5.
* **Base de Datos:** SQLite (Entorno de desarrollo).
* **Librerías Adicionales:** `Pillow` (Manejo de imágenes), `django-jazzmin` (Opcional, para estilizar el admin).

## 🔧 Instalación y Puesta en Marcha

Sigue estos pasos para correr el proyecto localmente:

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/tu-usuario/tienda-detalles-originales.git](https://github.com/tu-usuario/tienda-detalles-originales.git)
   cd tienda-detalles-originales
