import argparse
from app import flask_app

import os
import signal
import socketserver

import threading

from socket_server import server_running, client_sockets, CommandLineHandler
from utils import common_utils


def signal_handler(sig, frame):
    global server_running
    print("Ctrl+C pressed. Initiating server shutdown.")
    server_running.clear()

    # Notify all connected clients about the shutdown
    for client_socket in client_sockets:
        try:
            client_socket.sendall("Server is shutting down. Goodbye!".encode('utf-8'))
            client_socket.close()
        except Exception as e:
            print(f"Error notifying client about shutdown: {e}")

    os._exit(0)


def start_server(host, http_port, command_line_port, log_file):
    log_thread = threading.Thread(target=common_utils.log_writer, args=(log_file,server_running,))
    log_thread.start()

    log_message_start = f"Starting server"
    common_utils.log_queue.put(log_message_start)

    # # agregar getaddrinfo para poder hacerlo andar en ipv6
    flask_thread = threading.Thread(target=flask_app.run, kwargs={'host': host, 'port': http_port, 'threaded': True, 'use_reloader': False, 'debug': False})
    flask_thread.start()

    # Start the command-line server and log writer as before
    command_line_server = socketserver.ThreadingTCPServer((host, command_line_port), CommandLineHandler)
    command_line_thread = threading.Thread(target=command_line_server.serve_forever)
    command_line_thread.start()

    print(f'Servidor HTTP escuchando en puerto: {http_port}, command line escuchando en puerto: {command_line_port}')
    log_message_start = f"Servidor HTTP escuchando en puerto: {http_port}, command line escuchando en puerto: {command_line_port}"
    common_utils.log_queue.put(log_message_start)

    signal.signal(signal.SIGINT, signal_handler)

    # Wait for command-line server and log writer threads to finish before exiting
    flask_thread.join()
    command_line_thread.join()
    log_thread.join()


def main():
    parser = argparse.ArgumentParser(description='Multithreaded server')
    parser.add_argument('--host', type=str, default='localhost', help='Server host')
    parser.add_argument('--http_port', type=int, default=8080, help='HTTP port')
    parser.add_argument('--command_line_port', type=int, default=9090, help='Command-line port')
    parser.add_argument('--log_file', type=str, default='server.log', help='Log file path')
    args = parser.parse_args()

    start_server(args.host, args.http_port, args.command_line_port, args.log_file)


if __name__ == '__main__':
    main()