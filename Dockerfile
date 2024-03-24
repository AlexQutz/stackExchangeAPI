# Use the official Python image as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Redis server
RUN apt-get update && apt-get install -y redis-server

# Copy the Flask application code to the container
COPY . .

# Expose the port on which your Flask app runs
EXPOSE 5000

# Start Redis server and run the Flask application
CMD service redis-server start && python main.py