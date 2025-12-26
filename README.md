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
   
---

2. **Crear entorno virtual:**
   ```Bash
    # Windows
    python -m venv venv
    venv\Scripts\activate
    # Mac/Linux
    python3 -m venv venv
    source venv/bin/activate

3. **Instalar dependencias:**

Bash

pip install -r requirements.txt

4. **Configurar Base de Datos:**

Bash

python manage.py makemigrations
python manage.py migrate

4. **Crear Superusuario:**

Bash

python manage.py createsuperuser

5. **Ejecutar servidor:**

Bash

python manage.py runserver

## 🚀 Guía de Deploy (Render)

Configuración para despliegue en **Render**.

### Configuración del Servicio

* **Build Command:**
  ```bash
  pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate

* **Start Command:**
  ```bash
  gunicorn PRUEBA_3_HUERTA_DE_LA_CRUZ.wsgi:application


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
* **Librerías:** `Pillow`, `Requests`, `dj-database-url`.

---
*Desarrollado por Cristally & Miriah Huerta*
