# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /usr/src/

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       libpq-dev \
       gcc \
       libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY ./bob/requirements.txt ./bob/
RUN pip install --no-cache-dir -r ./bob/requirements.txt

# Copy the current directory contents into the container at /usr/src/app
COPY ./bob /usr/src/bob

# Expose port 5000 to the outside world
EXPOSE 5000

# Run the application with Gunicorn
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5000", "bob:app"]