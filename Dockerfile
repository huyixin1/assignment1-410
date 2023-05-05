# Use Python base image
FROM python:3.8

# Set the working directory to /app
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the necessary subdirectories and files to the /app directory in the container
COPY main.py /app
COPY main_modules /app/main_modules
COPY helper_modules /app/helper_modules

# Expose the ports for both services
EXPOSE 3000 3001

# Set the environment variable for the Flask app
ENV FLASK_APP=main

