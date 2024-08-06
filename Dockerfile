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
RUN pip install gunicorn

# Expose the port
EXPOSE 8000

# Run the Django server
CMD ["gunicorn", "_core.wsgi:application", "--bind", "0.0.0.0:8000"]
