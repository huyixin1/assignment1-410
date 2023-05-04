# Use the official Python base image
FROM python:3.8

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Expose the ports for both services
EXPOSE 3000 3001

# Set the environment variable for the Flask app
ENV FLASK_APP=main