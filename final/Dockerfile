# Use the official Python image as a base image
FROM python:3.9-slim

ARG HOST_IPV4
ARG HTTP_PORT_IPV4
ARG COMMAND_LINE_PORT_IPV4
ARG HOST_IPV6
ARG HTTP_PORT_IPV6
ARG COMMAND_LINE_PORT_IPV6
ARG LOG_FILE

ENV HOST_IPV4 ${HOST_IPV4}
ENV HTTP_PORT_IPV4 ${HTTP_PORT_IPV4}
ENV COMMAND_LINE_PORT_IPV4 ${COMMAND_LINE_PORT_IPV4}
ENV HOST_IPV6 ${HOST_IPV6}
ENV HTTP_PORT_IPV6 ${HTTP_PORT_IPV6}
ENV COMMAND_LINE_PORT_IPV6 ${COMMAND_LINE_PORT_IPV6}
ENV LOG_FILE ${LOG_FILE}

# Set the working directory in the container
WORKDIR /app

# Copy Pipfile and Pipfile.lock to the working directory
COPY requirements.txt ./
COPY src/ .

# Install dependencies using pipenv
RUN pip install -r requirements.txt
RUN pip install prometheus_client
RUN apt-get update && apt-get install -y procps && rm -rf /var/lib/apt/lists/*


# Expose ports 8082 and 9092
EXPOSE 8082 9092 8000

# Copy the rest of the application code to the working directory

# Command to run the Python application
# ENTRYPOINT [ "python", "-u", "main.py" ]

# CMD ["python", "-u", "main.py", \
#      "--host_ipv4", "0.0.0.0", \
#      "--http_port_ipv4", "8082", \
#      "--command_line_port_ipv4", "9092", \
#      "--host_ipv6", "::", \
#      "--http_port_ipv6", "8083", \
#      "--command_line_port_ipv6", "9093", \
#      "--log_file", "output.log"]

# Copy the entrypoint script
COPY entrypoint.sh /entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /entrypoint.sh

# Use the entrypoint script as the entrypoint
ENTRYPOINT ["/entrypoint.sh"]
