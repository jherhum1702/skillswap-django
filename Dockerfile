# Usa una imagen base ligera de Python
FROM python:3.14-slim

# Establece el directorio de trabajo
WORKDIR /app

# Instala dependencias del sistema necesarias para compliar paquetes como psycopg2
RUN apt-get update && apt-get install -y \
    gettext \
    build-essential \
    libpq-dev \
    gcc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Crea un usuario para evitar correr la app como root.
RUN groupadd -g 1000 django && useradd -m -u 1000 -g django django

# Copia el archivo de dependencias antes de copiar el código (mejora la caché de Docker)
COPY requirements.txt .

# Instala las dependendias de Python globalmente sin usar '--user'
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código fuente al contenedor
COPY . .

# Da permisos al usuario para evitar problemas con volúmenes
RUN chown -R django:django /app

# Expone el puerto que la aplicación usará
EXPOSE 8000

# Cambia al usuario no root para ejecutar la aplicación
USER django

# Comando para ejecutar la aplicación usando Gunicorn, un servidor WSGI recomendado para producción
CMD ["gunicorn", "skillswap.wsgi:application", "--bind", "0.0.0.0:8000"]

