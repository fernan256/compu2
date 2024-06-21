#!/bin/sh

# Run the Python application with the appropriate environment variables
exec python -u main.py \
    --host_ipv4 "$HOST_IPV4" \
    --http_port_ipv4 "$HTTP_PORT_IPV4" \
    --command_line_port_ipv4 "$COMMAND_LINE_PORT_IPV4" \
    --host_ipv6 "$HOST_IPV6" \
    --http_port_ipv6 "$HTTP_PORT_IPV6" \
    --command_line_port_ipv6 "$COMMAND_LINE_PORT_IPV6" \
    --log_file "$LOG_FILE"