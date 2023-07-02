# Utiliza la imagen base de Python
FROM python:3.9

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo requirements.txt al contenedor
COPY requirements.txt .

# Instala las dependencias de la aplicación
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código fuente de la aplicación al contenedor
COPY . .

# Expone el puerto 8000 para acceder a la aplicación
EXPOSE 8000

# Define el comando de inicio del contenedor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]