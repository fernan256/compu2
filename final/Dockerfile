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

WORKDIR /app

COPY requirements.txt ./
COPY src/ .

RUN pip install -r requirements.txt
RUN pip install prometheus_client
RUN apt-get update && apt-get install -y procps && rm -rf /var/lib/apt/lists/*


EXPOSE 8082 9092 8000

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
