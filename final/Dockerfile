# Use the official Python image as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy Pipfile and Pipfile.lock to the working directory
COPY requirements.txt ./
COPY src/ .

# Install dependencies using pipenv
RUN pip install -r requirements.txt

# Expose ports 8082 and 9092
EXPOSE 8082 9092

# Copy the rest of the application code to the working directory

# Command to run the Python application
CMD [ "python", "-u", "main.py", "--host", "0.0.0.0", "--http_port", "8082", "--command_line_port", "9092", "--log_file", "output.txt" ]
