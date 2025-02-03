# Usa la imagen base de Python 3.11.8
FROM python:3.11.8-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de requirements a la imagen
COPY requirements_linux.txt requirements.txt

# Instala las dependencias especificadas en requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el contenido de la carpeta actual a /app en el contenedor
COPY . .

# Expone el puerto que Streamlit utiliza (por defecto es el 8501)
EXPOSE 8501

# Comando para ejecutar la aplicación
CMD ["streamlit", "run", "src/app/app.py"]

# Construir la imagen: docker build -t [nombre_imagen] .
# Ejecutar el contenedor: docker run -p 8501:8501 [nombre_imagen]
# Acceder a la consola del contenedor: docker exec -it [id_contenedor] ../bin/bash
