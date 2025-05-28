# Dockerfile

FROM python:3.11

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libmariadb-dev \
    libmariadb-dev-compat \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos
COPY . .

# Actualizar pip
RUN pip install --upgrade pip

# Instalar requerimientos
RUN pip install -r requirements.txt

# Exponer puerto
EXPOSE 8000

# Comando para iniciar
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
