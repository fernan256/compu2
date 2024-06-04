import argparse
import socketserver
import threading
import time
import queue
import signal
import os
from concurrent.futures import ThreadPoolExecutor
from mysql_connector import get_db_session
from app import flask_app, Config
from utils import common_utils 
import subprocess
from sqlalchemy import text


server_running = threading.Event()
server_running.set()
client_sockets = []
scraper_executor = ThreadPoolExecutor(max_workers=5)  # Adjust the number of workers as needed


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
                common_utils.log_queue.put(log_message)
                print(f"Received command-line request from {self.client_address[0]}: {self.data.decode('utf-8')}")

                command = self.data.decode('utf-8')
                print(command)

                if command.lower() == 'shutdown':
                    print("Server is shutting down. Notifying client.")
                    client_socket.sendall("Server is shutting down. Goodbye!".encode('utf-8'))
                    break

                if command.startswith("LOGIN"):
                    _, username, password = command.split()
                    log_message = f"Login method"
                    common_utils.log_queue.put(log_message)

                    # connection = get_mysql_connection()
                    # if connection:
                    with get_db_session() as session:
                        try:
                            # cursor = connection.cursor()

                            result = session.execute(
                                text(f"SELECT * FROM user WHERE username = '{username}' AND password = '{password}'")
                            ).fetchone()

                            if result:
                                response = "Login successful! You can now interact with the server11111."
                                client_socket.sendall(response.encode('utf-8'))

                                options = "Seleccionar una opcion:\n1. Listar Recitales Guardados 1\n2. Buscar en paginas 2\n3. Editar Configuraciones de Usuario 3\n"  # Modify this line with your actual options
                                client_socket.sendall(options.encode('utf-8'))

                                while server_running.is_set():
                                    user_input = client_socket.recv(1024).strip().decode('utf-8')
                                    if user_input.lower() == 'exit':
                                        break

                                    response = f"Server received: {user_input}"
                                    print(f"received from client: {response}")
                                    print(f"going to start scrap for url {response}")
                                    client_socket.sendall(response.encode('utf-8'))

                                    # Call the ScrapperService for scraping
                                    scraper_executor.submit(scraper_service.start_scraper, response)

                                    # Handle response for each option
                                    # match user_input:
                                        # case 1:
                                        #     client_sockets[client_socket] = user_input
                                        #     client_socket.sendall(f"Option {user_input} selected.".encode('utf-8'))
                                    # if user_input in ['1', '2', '3']:
                                    #     client_sockets[client_socket] = user_input
                                    #     client_socket.sendall(f"Option {user_input} selected.".encode('utf-8'))

                            else:
                                response = "Login failed. Exiting thread."
                                client_socket.sendall(response.encode('utf-8'))
                                break  # Exit the loop if login fails
                        except Exception as e:
                            print(f"Error connecting: {e}")
                            response = "Failed to connect to the database. Exiting thread."
                            client_socket.sendall(response.encode('utf-8')) 
                            break
                        # finally:
                        #     cursor.close()

                    # else:
                    #     response = "Failed to connect to the database. Exiting thread."
                    #     client_socket.sendall(response.encode('utf-8'))
                    #     break  # Exit the loop if database connection fails

                elif command.startswith("SIGNUP"):
                    _, new_username, new_password, new_email = command.split()

                    # connection = get_mysql_connection()
                    with get_db_session() as session:
                        try:
                            # cursor = connection.cursor()

                            # Check if the username already exists
                            # cursor.execute(f" SELECT * FROM users WHERE username = ${new_username}")
                            # existing_user = cursor.fetchone()
                            existing_user = session.execute(
                                text(f"SELECT * FROM users WHERE username = '{new_username}'")
                            ).fetchone()

                            if existing_user:
                                response = "Username already exists. Please choose a different one."
                                client_socket.sendall(response.encode('utf-8'))
                            else:
                                # Insert the new user into the database
                                create_user = session.execute(text(f"INSERT INTO user (username, password, email) VALUES '{new_username}', '{new_password}', '{new_email}'"))
                                session.commit()

                                response = "Signup successful! You can now log in."
                                client_socket.sendall(response.encode('utf-8'))

                        # finally:
                        #     cursor.close()
                        except Exception as e:
                            print(f"Error connecting: {e}")
                            response = "Failed to connect to the database. Exiting thread."
                            client_socket.sendall(response.encode('utf-8')) 
                            break
                    # else:
                    #     response = "Failed to connect to the database. Exiting thread."
                    #     client_socket.sendall(response.encode('utf-8'))
                    #     break  # Exit the loop if database connection fails

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

# def signal_handler(sig, frame):
#     global server_running
#     print("Ctrl+C pressed. Initiating server shutdown.")
#     server_running.clear()

#     # Notify all connected clients about the shutdown
#     for client_socket in client_sockets:
#         try:
#             client_socket.sendall("Server is shutting down. Goodbye!".encode('utf-8'))
#             client_socket.close()
#         except Exception as e:
#             print(f"Error notifying client about shutdown: {e}")

#     os._exit(0)


# def start_server(host, http_port, command_line_port, log_file):
#     log_thread = threading.Thread(target=common_utils.log_writer, args=(log_file,server_running,))
#     log_thread.start()

#     log_message_start = f"Starting server"
#     common_utils.log_queue.put(log_message_start)

#     # # agregar getaddrinfo para poder hacerlo andar en ipv6
#     flask_thread = threading.Thread(target=flask_app.run, kwargs={'host': host, 'port': http_port, 'threaded': True, 'use_reloader': False, 'debug': False})
#     flask_thread.start()

#     # Start the command-line server and log writer as before
#     command_line_server = socketserver.ThreadingTCPServer((host, command_line_port), CommandLineHandler)
#     command_line_thread = threading.Thread(target=command_line_server.serve_forever)
#     command_line_thread.start()

#     print(f'Servidor HTTP escuchando en puerto: {http_port}, command line escuchando en puerto: {command_line_port}')
#     log_message_start = f"Servidor HTTP escuchando en puerto: {http_port}, command line escuchando en puerto: {command_line_port}"
#     common_utils.log_queue.put(log_message_start)

#     signal.signal(signal.SIGINT, signal_handler)

#     # Wait for command-line server and log writer threads to finish before exiting
#     flask_thread.join()
#     command_line_thread.join()
#     log_thread.join()

   