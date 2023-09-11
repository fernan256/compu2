import socketserver
import threading
import argparse

# Definicion de un custom handler para el servidor http
class MyHTTPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print(f"Received HTTP request from {self.client_address[0]}: {self.data.decode('utf-8')}")
        # Add your HTTP request handling logic here
        if self.data.startswith(b"GET"):
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nHello, World!\r\n"
            self.request.sendall(response.encode('utf-8'))
        else:
            response = "HTTP/1.1 400 Bad Request\r\nContent-Type: text/plain\r\n\r\nBad Request\r\n"
            self.request.sendall(response.encode('utf-8'))

# Definicion de un custom handler para el cliente de linea de comandos
class MyCommandLineHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print(f"Received command-line request from {self.client_address[0]}: {self.data.decode('utf-8')}")
        # Add your command-line request handling logic here

# Server
def start_server(host, http_port, command_line_port):
    # Creo servidor HTTP
    socketserver.TCPServer.allow_reuse_address = True
    http_server = socketserver.TCPServer((host, http_port), MyHTTPHandler)
    
    # Creo servidor de linea de comandos
    command_line_server = socketserver.TCPServer((host, command_line_port), MyCommandLineHandler)

    # Creo los threads para atender ambos servidores
    http_thread = threading.Thread(target=http_server.serve_forever)
    command_line_thread = threading.Thread(target=command_line_server.serve_forever)

    # Inicializo threads
    http_thread.start()
    command_line_thread.start()

    print(f"Servidor HTTP escuchando en puerto {http_port}")
    print(f"Servidor de linea de comandos escuchando en puerto {command_line_port}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Servidor multithread")
    parser.add_argument("--host", type=str, default="localhost", help="Nombre del host")
    parser.add_argument("--http_port", type=int, default=8080, help="Puerto para request HTTP")
    parser.add_argument("--command_line_port", type=int, default=9090, help="Puerto para requests de linea de comandos")
    args = parser.parse_args()

    start_server(args.host, args.http_port, args.command_line_port)