# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the project files
COPY . /app/

# Collect static files
#RUN python manage.py collectstatic --noinput

# Install Gunicorn and Uvicorn
RUN pip install gunicorn uvicorn


# Command to run the application using Gunicorn with UvicornWorker
# CMD ["gunicorn", "_core.asgi:application", "--bind", "0.0.0.0:8080", "--worker-class", "uvicorn.workers.UvicornWorker"]

CMD ["gunicorn", "_core.asgi:application", "-k", "uvicorn.workers.UvicornWorker"]