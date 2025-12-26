# Tienda Detalles Originales 🌷

> Sistema web integral para la gestión de pedidos personalizados y control de inventario, desarrollado con Django.

[![Deploy Status](https://img.shields.io/badge/Deploy-Render-success)](https://tienda-detalles-originales-re9w.onrender.com/catalogo/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0-green)](https://www.djangoproject.com/)

## 📖 Descripción del Proyecto

La **Tienda Detalles Originales** es una solución web diseñada para optimizar el flujo de trabajo de una tienda de artículos personalizados (poleras, tazones, impresiones 3D).

El sistema centraliza la gestión de pedidos que llegan por diversos canales (WhatsApp, RRSS, presencial) en un único panel de administración. Además, ofrece a los clientes una plataforma web para visualizar el catálogo, solicitar cotizaciones y realizar seguimiento en tiempo real de sus compras.

**URL Pública del Sistema:** [https://tienda-detalles-originales-re9w.onrender.com/catalogo/](https://tienda-detalles-originales-re9w.onrender.com/catalogo/)

---

## ✨ Características Principales

### 🛍️ Cliente (Vistas Públicas)
* **Catálogo Visual:** Galería filtrable por categorías (Ropa, Hogar, 3D).
* **Solicitud de Pedidos:** Formulario para subir imágenes de referencia y solicitar productos personalizados.
* **Seguimiento (Tracking):** Sistema de consulta de estado del pedido mediante un Token único.

### 🛠️ Administración (Back-office)
* **Gestión Centralizada:** Administración de pedidos de múltiples canales.
* **Inventario:** Control de insumos críticos (stock de poleras, filamento, etc.).
* **Ciclo de Vida:** Flujo de estados (Solicitado → Aprobado → En Proceso → Entregado).
* **API REST:** Endpoints para integración y consulta de datos desde aplicaciones externas.

---

## 🔧 Instalación y Puesta en Marcha (Local)

Pasos para ejecutar el proyecto en entorno de desarrollo:

### Prerrequisitos
* Python 3.10 o superior
* Git

### Pasos
1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/Cristally/Tienda-Detalles-Originales-.git](https://github.com/Cristally/Tienda-Detalles-Originales-.git)
   cd Tienda-Detalles-Originales-
   cd PRUEBA_3_HUERTA_DE_LA_CRUZ

2. **Crear entorno virtual:**
   ```Bash
    # Windows
    python -m venv venv
    venv\Scripts\activate
   
    # Mac/Linux
    python3 -m venv venv
    source venv/bin/activate

3. **Instalar dependencias:**
   ```Bash
   pip install -r requirements.txt

4. **Configurar Base de Datos:**
   ```Bash
      python manage.py makemigrations
      python manage.py migrate

4. **Crear Superusuario:**
   ```Bash
      python manage.py createsuperuser

5. **Ejecutar servidor:**
   ```Bash
      python manage.py runserver

---

## 🚀 Guía de Deploy (Render)

Configuración para despliegue en **Render**.

### Configuración del Servicio

* **Build Command:**
  ```bash
  pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate

* **Start Command:**
  ```bash
  gunicorn PRUEBA_3_HUERTA_DE_LA_CRUZ.wsgi:application

--- 

### Variables de Entorno (Environment Variables)

Configurar en el dashboard de Render:

| Variable | Valor |
| :--- | :--- |
| `PYTHON_VERSION` | `3.10.0` |
| `SECRET_KEY` | *[Tu clave secreta]* |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `tienda-detalles-originales-re9w.onrender.com` |
| `DATABASE_URL` | *[Auto-configurado por Render]* |

## 🎨 Tecnologías Utilizadas

* **Backend:** Python, Django 5.0, Django REST Framework.
* **Frontend:** HTML5, CSS3, Bootstrap 5.
* **Base de Datos:** SQLite (Dev) / PostgreSQL (Prod).
* **Servidor:** Gunicorn, Whitenoise.

| Libreria | Función | Instalación |
| :--- | :--- | :--- |
| `djangorestframework` | Libreria basíca para configuración e implementación de la API | `pip install djangorestframework` |
| `django` | *Framework para Backend* | `pip install django` |
| `django-colorfield` | Libreria para la utilización de un color picker | `pip install django-colorfield` |
| `pillow` | Permite el manejo adecuado de imagenes dentro de la base de datos | `pip install pillow` |
| `whitenoise` | Ayuda a la gestión de imagenes estaticas | `pip install whitenoise` |
| `reportlab` | Generación de archivos en formato PDF | `pip install reportlab` |
| `drf_spectacular` | Permite mostrar documentación de API | `pip install drf-spectacular` |
| `requests` | Permite realizar consultas a la API | `pip install requests` |

---

## 🔐 Credenciales de acceso

| Usuario | Contraseña | Rol |
| :--- | :--- | :--- |
| `admin` | `admin` | `Administrador` |
| `cliente` | `Hola12345` | `Usuario` |
| `Token de seguimiento` | `-----` | `459d1609-54cb-46fb-bab1-1d1102f3a906` |

---

## 📖 Endpoints de Categorías

| Metodo | Autenticación Sí/No | Endpoint |
| :--- | :--- | :--- |
| `GET` | `Sí` | `/api/categorias/` |
| `PUT` | `Sí` | `/api/categorias/{id}/` |
| `PATCH` | `Sí` | `/api/categorias/{id}/` |
| `DELETE` | `Sí` | `/api/categorias/{id}/delete/` |
| `GET` | `Sí` | `/api/categorias/crear/` |
| `POST` | `Sí` | `/api/categorias/crear/` |

---

## 🧶 Endpoints de Insumos

| Metodo | Autenticación Sí/No | Endpoint |
| :--- | :--- | :--- |
| `GET` | `Sí` | `/api/insumos/` |
| `GET` | `Sí` | `/api/insumos/{id}/` |
| `PUT` | `Sí` | `/api/insumos/{id}/` |
| `PATCH` | `Sí` | `/api/insumos/{id}/` |
| `DELETE` | `Sí` | `/api/insumos/{id}/delete/` |
| `GET` | `Sí` | `/api/insumos/crear/` |
| `POST` | `Sí` | `/api/insumos/crear/` |
| `GET` | `Sí` | `/api/insumos/filtrar/{nombre}/` |

---

## 📬 Endpoints de Pedidos

| Metodo | Autenticación Sí/No | Endpoint |
| :--- | :--- | :--- |
| `PUT` | `Sí` | `/api/pedidos/{id}/` |
| `PATCH` | `Sí` | `/api/pedidos/{id}/` |
| `POST` | `Sí` | `/api/pedidos/crear/` |
| `GET` | `Sí` | `/api/pedidos/filtrar/{token}/` |
| `GET` | `Sí` | `/api/pedidos/filtrar/estado/{estado_pedido}/` |
| `GET` | `Sí` | `/api/pedidos/filtrar/estado_pago/{estado_pago}/` |
| `GET` | `Sí` | `/api/pedidos/filtrar/por-fecha/` |

---

## 📦 Endpoints de Productos

| Metodo | Autenticación Sí/No | Endpoint |
| :--- | :--- | :--- |
| `GET` | `Sí` | `/api/productos/` |
| `POST` | `Sí` | `/api/productos/` |
| `PUT` | `Sí` | `/api/productos/{id}/` |
| `PATCH` | `Sí` | `/api/productos/{id}/` |
| `DELETE` | `Sí` | `/api/productos/{id}/delete/` |
| `GET` | `Sí` | `/api/productos/crear/` |
| `POST` | `Sí` | `/api/productos/crear/` |


---

### Pasos para desplegar interfaz con listado de endpoints
1. **Instalar drf-spectacular:**
   ```bash
      pip install drf-spectacular

2. **Añadirlo a INSTALLED APPS en Settings.py**
   ```Bash
   INSTALLED_APPS = [
       'django.contrib.admin',
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       'django.contrib.messages',
       'django.contrib.staticfiles',
       'appTienda',
       'rest_framework',
       'drf_spectacular',
       'colorfield', 
   ]

3. **Añadir opciones de configuración en Settings.py**
   ```Bash
   REST_FRAMEWORK = {
       'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',}
   
   SPECTACULAR_SETTINGS = {
       'TITLE': 'API Tienda',
       'DESCRIPTION': 'Documentación de la API',
       'VERSION': '1.0.0',}

4. **Dirigirse al endpoint:**
   ```Bash
   http://127.0.0.1:8000/api/docs/

Es posible descargar el archivo en [formato .yaml](endpoints/Endpoints.yaml) o en [formato .json](endpoints/Endpoints.json)


---


*Desarrollado por Stephany de la Cruz & Miriah Huerta*

