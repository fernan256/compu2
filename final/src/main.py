import argparse
import os
import psutil
import signal
import socketserver
import socket
import time
import threading

from prometheus_client import start_http_server, Summary, Counter, Gauge
from socket_server import server_running, client_sockets, CommandLineHandler

from app import flask_app
from utils import common_utils


REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
REQUEST_COUNTER = Counter('request_count', 'Total request count')
THREAD_COUNT = Gauge('thread_count', 'Number of threads in use')
MEMORY_USAGE = Gauge('memory_usage', 'Memory usage in bytes')


class IPv6TCPServer(socketserver.ThreadingTCPServer):
    address_family = socket.AF_INET6


class IPv4TCPServer(socketserver.ThreadingTCPServer):
    address_family = socket.AF_INET


def execute_p_socket(host, port, address_family, handler):
    socketserver.TCPServer.allow_reuse_address = True
    if address_family == socket.AF_INET:
        print("ipv4")
        server = IPv4TCPServer((host, port), handler)
    elif address_family == socket.AF_INET6:
        print("ipv6")
        server = IPv6TCPServer((host, port), handler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
    return server_thread


def start_metrics_server():
    start_http_server(8000)
    while True:
        THREAD_COUNT.set(threading.active_count())
        MEMORY_USAGE.set(psutil.Process(os.getpid()).memory_info().rss)
        time.sleep(1)


def start_server(host_ipv4, http_port_ipv4, command_line_port_ipv4, host_ipv6, http_port_ipv6, command_line_port_ipv6, log_file):
    log_thread = threading.Thread(target=common_utils.log_writer, args=(log_file, server_running,))
    log_thread.start()

    log_message_start = "Starting server"
    common_utils.log_queue.put(log_message_start)

    # Update Flask app to bind to both IPv4 and IPv6
    flask_thread_ipv4 = threading.Thread(target=flask_app.run, kwargs={'host': host_ipv4, 'port': int(http_port_ipv4), 'threaded': True, 'use_reloader': False, 'debug': False})
    flask_thread_ipv6 = threading.Thread(target=flask_app.run, kwargs={'host': host_ipv6, 'port': int(http_port_ipv6), 'threaded': True, 'use_reloader': False, 'debug': False})
    flask_thread_ipv4.start()
    flask_thread_ipv6.start()

    command_line_thread_ipv4 = execute_p_socket(host_ipv4, int(command_line_port_ipv4), socket.AF_INET, CommandLineHandler)
    command_line_thread_ipv6 = execute_p_socket(host_ipv6, int(command_line_port_ipv6), socket.AF_INET6, CommandLineHandler)

    metrics_thread = threading.Thread(target=start_metrics_server)
    metrics_thread.start()

    print(f'Servidor HTTP escuchando IPV4 en puerto: {http_port_ipv4}, Servidor CMD escuchando IPV4 en puerto: {command_line_port_ipv4}')
    log_message_start_ipv4 = f"Servidor HTTP escuchando IPV4 en puerto: {http_port_ipv4}, Servidor CMD escuchando IPV4 en puerto: {command_line_port_ipv4}"
    common_utils.log_queue.put(log_message_start_ipv4)

    print(f'Servidor HTTP escuchando IPV6 en puerto: {http_port_ipv6}, Servidor CMD escuchando IPV6 en puerto: {command_line_port_ipv6}')
    log_message_start_ipv6 = f"Servidor HTTP escuchando IPV6 en puerto: {http_port_ipv6}, Servidor CMD escuchando IPV6 en puerto: {command_line_port_ipv6}"
    common_utils.log_queue.put(log_message_start_ipv6)


    flask_thread_ipv4.join()
    flask_thread_ipv6.join()
    command_line_thread_ipv4.join()
    command_line_thread_ipv6.join()
    log_thread.join()
    metrics_thread.join()

def main():
    parser = argparse.ArgumentParser(description='Multithreaded server')
    parser.add_argument('--host_ipv4', type=str, default='::', help='Server host')
    parser.add_argument('--http_port_ipv4', type=str, default='8080', help='HTTP port')
    parser.add_argument('--command_line_port_ipv4', type=str, default='9090', help='Command-line port')
    parser.add_argument('--host_ipv6', type=str, default='::', help='Server host')
    parser.add_argument('--http_port_ipv6', type=str, default='8081', help='HTTP port')
    parser.add_argument('--command_line_port_ipv6', type=str, default='9091', help='Command-line port')
    parser.add_argument('--log_file', type=str, default='server.log', help='Log file path')
    args = parser.parse_args()

    start_server(args.host_ipv4, args.http_port_ipv4, args.command_line_port_ipv4, args.host_ipv6, args.http_port_ipv6, args.command_line_port_ipv6, args.log_file)

if __name__ == '__main__':
    main()
