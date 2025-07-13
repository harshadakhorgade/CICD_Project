
# Use slim base image
FROM python:3.10-slim

# Set workdir
WORKDIR /app

# Install system dependencies (only if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .

# Install dependencies without cache
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose port
EXPOSE 8000

# Use Gunicorn for production server
CMD ["gunicorn", "bookstore_project.wsgi:application", "--bind", "0.0.0.0:8000"]



# simple -----

# # Use the official Python image
# FROM python:3.10-slim

# # Set the working directory in the container
# WORKDIR /app

# # Copy the requirements file and install dependencies
# COPY requirements.txt .
# RUN pip install -r requirements.txt

# # Copy the entire project into the container
# COPY . .

# # Expose port 8000 for the Django development server
# EXPOSE 8000

# # Default command to run the Django server
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]