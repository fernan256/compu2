import socketserver
import threading
import argparse
import queue
import signal
import os

# Creo la queue para guardar los logs
log_queue = queue.Queue()
server_running = True


def log_writer(log_file):
    while server_running:
        try:
            log_message = log_queue.get()
            if log_message is None:
                break
            with open(log_file, 'a') as f:
                f.write(log_message + '\n')
        except queue.Empty:
            pass


# Definicion de un custom handler para el servidor http
class MyHTTPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        log_message = f"Received HTTP request from {self.client_address[0]}: {self.data.decode('utf-8')}"
        log_queue.put(log_message)
        print(f"Received HTTP request from {self.client_address[0]}: {self.data.decode('utf-8')}")
        # Logica para http, aca voy a hacer el manejo de las paginas
        if self.data.startswith(b"GET"):
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nHello, World!\r\n"
            self.request.sendall(response.encode('utf-8'))
        else:
            response = "HTTP/1.1 400 Bad Request\r\nContent-Type: text/plain\r\n\r\nBad Request\r\n"
            self.request.sendall(response.encode('utf-8'))

# Definicion de un custom handler para el cliente de linea de comandos
class CommandLineHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while server_running:
            self.data = self.request.recv(1024).strip()
            print(f"server_running: {server_running}")
            log_message = f"Received command-line request from {self.client_address[0]}: {self.data.decode('utf-8')}"
            log_queue.put(log_message)
            print(f"Received command-line request from {self.client_address[0]}: {self.data.decode('utf-8')}")
            # Logica para linea de comandos, aca va a estar la parte para triggear login y scrapping
            if server_running:
                self.request.close()
                return

        self.request.close()


# Funcion para manejar el ctrl+c
def signal_handler(sig, frame):
    global server_running
    print("Ctrl+C pressed. Exiting command-line handler gracefully.")
    server_running = False
    os._exit(0)


# Server
def start_server(host, http_port, command_line_port, log_file):
    # Creo servidor HTTP
    socketserver.TCPServer.allow_reuse_address = True
    http_server = socketserver.TCPServer((host, http_port), MyHTTPHandler)
    
    # Creo servidor de linea de comandos
    command_line_server = socketserver.TCPServer((host, command_line_port), CommandLineHandler)

    # Creo los threads para atender ambos servidores
    http_thread = threading.Thread(target=http_server.serve_forever)
    command_line_thread = threading.Thread(target=command_line_server.serve_forever)

    print(f"HTTP server listening on {host}:{http_port}")
    print(f"Command-line server listening on {host}:{command_line_port}")

    # Creo el thread que se va a encargar de manejar el logueo
    log_thread = threading.Thread(target=log_writer, args=(log_file,))
    log_thread.start()

    signal.signal(signal.SIGINT, signal_handler)

    log_thread = threading.Thread(target=log_writer, args=(log_file,))

    # Inicializo threads
    http_thread.start()
    command_line_thread.start()
    log_thread.start()

    print(f"Servidor HTTP escuchando en puerto {http_port}")
    print(f"Servidor de linea de comandos escuchando en puerto {command_line_port}")

    # try:
    #     while server_running:
    #         command_line_server.handle_request()
    # except KeyboardInterrupt:
    #     pass

    # command_line_server.server_close()
    # log_queue.put(None)
    # log_thread.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Servidor multithread")
    parser.add_argument("--host", type=str, default="localhost", help="Nombre del host")
    parser.add_argument("--http_port", type=int, default=8080, help="Puerto para request HTTP")
    parser.add_argument("--command_line_port", type=int, default=9090, help="Puerto para requests de linea de comandos")
    parser.add_argument("--log_file", type=str, default="server.log", help="Log file path")
    args = parser.parse_args()

    start_server(args.host, args.http_port, args.command_line_port, args.log_file)