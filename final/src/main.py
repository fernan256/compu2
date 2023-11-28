import socketserver
import threading
import argparse
import queue
import signal
import os
from concurrent.futures import ThreadPoolExecutor

from mysql_connector import get_mysql_connection

log_queue = queue.Queue()
server_running = threading.Event()
server_running.set()  # Set the event to true initially
client_sockets = []
scraper_executor = ThreadPoolExecutor(max_workers=5)  # Adjust the number of workers as needed

def log_writer(log_file):
    while server_running.is_set():
        try:
            log_message = log_queue.get()
            if log_message is None:
                break
            with open(log_file, 'a') as f:
                f.write(log_message + '\n')
        except queue.Empty:
            pass

class MyHTTPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        log_message = f"Received HTTP request from {self.client_address[0]}: {self.data.decode('utf-8')}"
        log_queue.put(log_message)
        print(f"Received HTTP request from {self.client_address[0]}: {self.data.decode('utf-8')}")
        if self.data.startswith(b"GET"):
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nHello, World!\r\n"
            self.request.sendall(response.encode('utf-8'))
        else:
            response = "HTTP/1.1 400 Bad Request\r\nContent-Type: text/plain\r\n\r\nBad Request\r\n"
            self.request.sendall(response.encode('utf-8'))

class ScrapperService:
    def __init__(self):
        self.running = False

    def start_scraper(self, url):
        if not self.running:
            self.running = True
            try:
                # Simulate scraping by sleeping for a short duration
                print(f"Scraping for URL: {url}")
                time.sleep(2)  # Placeholder for actual scraping logic
                print(f"Scraping complete for URL: {url}")
            finally:
                self.running = False

scraper_service = ScrapperService()

class CommandLineHandler(socketserver.BaseRequestHandler):
    def handle(self):
        client_socket = self.request
        client_sockets.append(client_socket)

        while server_running.is_set():
            try:
                self.data = client_socket.recv(1024).strip()
                if not self.data:
                    break

                log_message = f"Received command-line request from {self.client_address[0]}: {self.data.decode('utf-8')}"
                log_queue.put(log_message)
                print(f"Received command-line request from {self.client_address[0]}: {self.data.decode('utf-8')}")

                command = self.data.decode('utf-8')
                print(command)

                if command.lower() == 'shutdown':
                    print("Server is shutting down. Notifying client.")
                    client_socket.sendall("Server is shutting down. Goodbye!".encode('utf-8'))
                    break

                if command.startswith("LOGIN"):
                    _, username, password = command.split()

                    connection = get_mysql_connection()
                    if connection:
                        try:
                            cursor = connection.cursor()

                            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
                            result = cursor.fetchone()

                            if result:
                                response = "Login successful! You can now interact with the server11111."
                                client_socket.sendall(response.encode('utf-8'))

                                while server_running.is_set():
                                    user_input = client_socket.recv(1024).strip().decode('utf-8')
                                    if user_input.lower() == 'exit':
                                        break

                                    response = f"Server received: {user_input}"
                                    print(f"received from client: {response}")
                                    print(f"going to start scrap for url {response}")

                                    # Call the ScrapperService for scraping
                                    scraper_executor.submit(scraper_service.start_scraper, response)

                                    client_socket.sendall(response.encode('utf-8'))

                            else:
                                response = "Login failed. Exiting thread."
                                client_socket.sendall(response.encode('utf-8'))
                                break  # Exit the loop if login fails

                        finally:
                            cursor.close()

                    else:
                        response = "Failed to connect to the database. Exiting thread."
                        client_socket.sendall(response.encode('utf-8'))
                        break  # Exit the loop if database connection fails

                elif command.startswith("SIGNUP"):
                    _, new_username, new_password, new_email = command.split()

                    connection = get_mysql_connection()
                    if connection:
                        try:
                            cursor = connection.cursor()

                            # Check if the username already exists
                            cursor.execute("SELECT * FROM users WHERE username = %s", (new_username,))
                            existing_user = cursor.fetchone()

                            if existing_user:
                                response = "Username already exists. Please choose a different one."
                                client_socket.sendall(response.encode('utf-8'))
                            else:
                                # Insert the new user into the database
                                cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (new_username, new_password, new_email))
                                connection.commit()

                                response = "Signup successful! You can now log in."
                                client_socket.sendall(response.encode('utf-8'))

                        finally:
                            cursor.close()

                    else:
                        response = "Failed to connect to the database. Exiting thread."
                        client_socket.sendall(response.encode('utf-8'))
                        break  # Exit the loop if database connection fails

                else:
                    response = "Invalid command."
                    client_socket.sendall(response.encode('utf-8'))

            except BrokenPipeError:
                print("Client disconnected unexpectedly.")
                break  # Exit the loop if BrokenPipeError occurs

            except Exception as e:
                print(f"Error handling command: {e}")
                break  # Exit the loop if an unexpected error occurs

        client_sockets.remove(client_socket)
        client_socket.close()

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
    # Creo servidor HTTP
    socketserver.TCPServer.allow_reuse_address = True
    http_server = socketserver.ThreadingTCPServer((host, http_port), MyHTTPHandler)

    # Creo servidor de linea de comandos
    command_line_server = socketserver.ThreadingTCPServer((host, command_line_port), CommandLineHandler)

    # Creo los threads para atender ambos servidores
    http_thread = threading.Thread(target=http_server.serve_forever)
    command_line_thread = threading.Thread(target=command_line_server.serve_forever)

    print(f"HTTP server listening on {host}:{http_port}")
    print(f"Command-line server listening on {host}:{command_line_port}")

    # Creo el thread que se va a encargar de manejar el logueo
    log_thread = threading.Thread(target=log_writer, args=(log_file,))
    log_thread.start()

    signal.signal(signal.SIGINT, signal_handler)

    # Inicializo threads
    http_thread.start()
    command_line_thread.start()
    log_thread.join()

    print(f"Servidor HTTP escuchando en puerto {http_port}")
    print(f"Servidor de linea de comandos escuchando en puerto {command_line_port}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multithreaded server")
    parser.add_argument("--host", type=str, default="localhost", help="Server host")
    parser.add_argument("--http_port", type=int, default=8080, help="HTTP port")
    parser.add_argument("--command_line_port", type=int, default=9090, help="Command-line port")
    parser.add_argument("--log_file", type=str, default="server.log", help="Log file path")
    args = parser.parse_args()

    start_server(args.host, args.http_port, args.command_line_port, args.log_file)
