# Puracultura
MultiVendor Ecommerce Django

## Prerrequisitos

- Python 3.11.6
- pip
- Virtualenv (opcional, pero recomendado)

## Instalación

Para configurar un entorno de desarrollo local, sigue estos pasos:

1. Clona el repositorio.
2. Crea un entorno virtual utilizando Python 3.11.6.
3. Activa el entorno virtual.
4. Instala las dependencias: `pip install -r requirements.txt`.

## Configuración del Proyecto

Después de instalar las dependencias, puedes seguir estos pasos para configurar el proyecto:

1. Configura las variables de entorno necesarias (por ejemplo, `SECRET_KEY`, configuración de la base de datos, etc.).
2. Realiza las migraciones necesarias con `python manage.py makemigrations` y `python manage.py migrate`.
3. Crea un superusuario con `python manage.py createsuperuser` si es necesario.
4. Ejecuta el servidor de desarrollo con `python manage.py runserver`.

Ahora, el proyecto debería estar corriendo en `http://127.0.0.1:8000/` en tu navegador.

## Notas Adicionales

- Asegúrate de no subir al repositorio información sensible como claves secretas o credenciales.
- Este proyecto está desarrollado con Django 4.2.7, asegúrate de revisar la documentación oficial de Django para más detalles.
