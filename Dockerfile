# Use the official Python image as the base image
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the Flask application files to the container's working directory
COPY ./app /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the required Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that your Flask application will listen on
EXPOSE 5000

# Command to run the Flask application (adjust as per your app structure)
CMD ["python", "app.py"]
