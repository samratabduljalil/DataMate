# Use a slim Python 3.10 image for a smaller footprint
FROM python:3.10

# Create a working directory for the application
WORKDIR /app

# Copy the requirements.txt file
COPY requirements.txt ./

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install missing dependency for OpenGL functionalities
RUN apt-get update && apt-get install -y libgl1-mesa-glx

# Copy the application code
COPY . .

# Expose the port used by FastAPI (typically 8000)
EXPOSE 8000

# Run the main application script (assuming it's named main.py)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]