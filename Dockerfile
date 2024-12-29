# Use a Python 3.10 image 
FROM python:3.10

# Create a working directory for the application
WORKDIR /app

# Copy only the app_for_docker.py file
COPY app_for_docker.py .

# Install dependencies from requirements.txt (if any)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install missing dependency for OpenGL functionalities (if needed)
RUN apt-get update && apt-get install -y libgl1-mesa-glx

# Expose the port used by FastAPI (typically 8000)
EXPOSE 8000

# Run the main application script
CMD ["uvicorn", "app_for_docker:app", "--host", "0.0.0.0", "--port", "8000"]