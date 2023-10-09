# Use the base Python image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the contents of the project directory into the container
COPY ./Life_ID /app

# Install dependencies in the container
RUN pip install -r requirements.txt

# Expose the port of the flaskapp.py
EXPOSE 2024

# Command to start the application
CMD ["python3", "flaskapp.py"]
