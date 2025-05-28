# Usa imagen base de Python
FROM python:3.10-slim

# Crea y usa un directorio de trabajo
WORKDIR /app

# Copia los archivos del backend
COPY . /app

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto del backend
EXPOSE 5000

# Comando para ejecutar la app Flask
CMD ["python", "app.py"]
