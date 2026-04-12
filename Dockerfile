# Usamos una imagen oficial de Python ligera
FROM python:3.12-slim

# Variables de entorno para que Python no escriba .pyc y no use buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalamos las librerías del sistema necesarias para compilar mysqlclient
RUN apt-get update \
    && apt-get install -y gcc default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Instalamos Poetry
RUN pip install poetry

# Establecemos el directorio de trabajo
WORKDIR /app

# Copiamos los archivos de dependencias
COPY pyproject.toml poetry.lock /app/

# Configuramos Poetry para que no cree un entorno virtual dentro del contenedor (no hace falta)
RUN poetry config virtualenvs.create false \
    && poetry add mysqlclient gunicorn \
    && poetry install --no-root --no-interaction --no-ansi

# Copiamos el resto de tu código Django
COPY . /app/

# Exponemos el puerto
EXPOSE 8000

# Comando para producción
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]