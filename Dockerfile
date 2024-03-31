# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy all files from the current directory to the /app directory in the container
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Expose the port on which the FastAPI application will run
EXPOSE 8000

# Command to run the FastAPI application using Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
