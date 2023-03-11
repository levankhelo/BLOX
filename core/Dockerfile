# Use a Python 3.8 base image
FROM python:3.8-slim-buster

# Install necessary packages
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx libglib2.0-dev && \
    apt-get clean

# Set working directory
WORKDIR /app

# Copy application files
COPY requirements.txt /app
COPY main.py /app

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Set up shared directory
RUN mkdir /shared

# Set up entrypoint
CMD ["python", "main.py"]
