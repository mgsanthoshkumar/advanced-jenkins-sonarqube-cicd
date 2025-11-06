# Use a minimal Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the application code into the container
COPY app.py /app/

# Define the command to run when the container starts
CMD ["python", "app.py"]
