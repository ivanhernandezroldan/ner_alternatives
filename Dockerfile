# Use Python 3.11.8 base image
FROM python:3.11.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements files to the image
COPY requirements_linux.txt requirements.txt

# Install dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy all content from current folder to /app in the container
COPY . .

# Expose the port that Streamlit uses (default is 8501)
EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "src/app/app.py"]

# Build the image: docker build -t [image_name] .
# Run the container: docker run -p 8501:8501 [image_name]
# Access container console: docker exec -it [container_id] ../bin/bash
