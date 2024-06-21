import getpass
import argparse
import socketserver
import sys
import threading
import time
import queue
import signal
import os
from app import flask_app, Config
from utils import common_utils 
import subprocess
from sqlalchemy import text
from app.models import Recitals
from app.services import services
from scrappers import save_recitals


server_running = threading.Event()
server_running.set()
client_sockets = []


def signal_handler(sig, frame):
    print('Received Ctrl+C (SIGINT) to stop the server')
    for client in client_sockets:
        try:
            client.sendall(b'SERVER_SHUTDOWN')
            client.close()
        except Exception as e:
            print(f"Error sending shutdown message to client: {e}")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler) 


class CommandLineHandler(socketserver.BaseRequestHandler):
    def handle(self):
        client_socket = self.request
        client_sockets.append(client_socket)

        while server_running.is_set():
            try:
                prompt = "Que quiere realizar LOGIN or SIGNUP? (type 'exit' to quit): "
                client_socket.sendall(prompt.encode('utf-8'))

                self.data = client_socket.recv(1024).strip()
                if not self.data:
                    break
                print(f'data: {self.data}')
                command = self.data.decode('utf-8').lower()
                
                if command == 'exit':
                    break
                
                if command == 'login':
                    self.handle_login(client_socket)

                elif command == 'signup':
                    self.handle_signup(client_socket)

                else:
                    response = "Invalid command."
                    client_socket.sendall(response.encode('utf-8'))

            except BrokenPipeError:
                print("Client disconnected unexpectedly.")
                break

            except Exception as e:
                print(f"Error handling command: {e}")
                break

        client_sockets.remove(client_socket)
        client_socket.close()


    def handle_login(self, client_socket):
        client_socket.sendall("Enter username: ".encode('utf-8'))
        username = client_socket.recv(1024).strip().decode('utf-8')

        client_socket.sendall("Enter password: ".encode('utf-8'))
        password = client_socket.recv(1024).strip().decode('utf-8')

        log_message = f"Login method"
        common_utils.log_queue.put(log_message)

        try:
            user = services.authenticate_user(username, password)
            if user:
                response = "Login successful! You can now interact with the server."
                client_socket.sendall(response.encode('utf-8'))

                options = ("Seleccionar una opcion:\n"
                            "1. Listar Recitales Guardados\n"
                            "2. Buscar en paginas\n"
                            "3. Editar Configuraciones de Usuario\n"
                            "4. Actualizar recitales\n"
                            "Type 'exit' to logout.\n")
                client_socket.sendall(options.encode('utf-8'))

                while server_running.is_set():
                    user_input = client_socket.recv(1024).strip().decode('utf-8')
                    if user_input.lower() == 'exit':
                        break
                    if user_input == '1':
                        self.list_recitals(client_socket, options, user.id)
                    elif user_input == '2':
                        self.search_recitals(client_socket, options)
                    elif user_input == '3':
                        self.edit_configurations(client_socket, options)
                    elif user_input == '4':
                        self.trigger_scraper_process(client_socket, options)
                    else:
                        client_socket.sendall("Command not recognized. Please try again.".encode('utf-8'))
                        client_socket.sendall(options.encode('utf-8'))
            else:
                response = "Login failed. Exiting thread."
                client_socket.sendall(response.encode('utf-8'))
        except Exception as e:
            print(f"Error connecting: {e}")
            response = "Failed to connect to the database. Exiting thread."
            client_socket.sendall(response.encode('utf-8'))


    def handle_signup(self, client_socket):
        client_socket.sendall("Enter new username: ".encode('utf-8'))
        new_username = client_socket.recv(1024).strip().decode('utf-8')

        client_socket.sendall("Enter new password: ".encode('utf-8'))
        new_password = client_socket.recv(1024).strip().decode('utf-8')

        client_socket.sendall("Enter new email: ".encode('utf-8'))
        new_email = client_socket.recv(1024).strip().decode('utf-8')

        try:
            newUser = services.create_user(new_username, new_password, new_email)
            print(newUser)

        except Exception as e:
            print(f"Error connecting: {e}")
            response = f"{e}. Exiting thread."
            client_socket.sendall(response.encode('utf-8'))


    def list_recitals(self, client_socket, options, user_id):
        try:
            page_option = "Pagina: "
            client_socket.sendall(page_option.encode('utf-8'))
            user_input2 = client_socket.recv(1024).strip().decode('utf-8')
            parts = user_input2.split()
            page = int(parts[0])
            per_page = int(parts[1]) if len(parts) > 1 else 10
            recitals, favorites, total = services.get_recitals(user_id, page=page, per_page=per_page)
            table_header = "ID | Artist | Date | Venue | Link\n"
            table_rows = []
            for recital in recitals:
                date = recital.date.strftime('%Y-%m-%d') if recital.date else ''
                row = f"{recital.id} | {recital.artist} | {date} | {recital.venue} | {recital.link}\n"
                table_rows.append(row)
            table = table_header + ''.join(table_rows)
            client_socket.sendall((table + '\n\n\n' + options).encode('utf-8'))
        except Exception as e:
            print(f"Error listing recitals: {e}")
            client_socket.sendall("Error listing recitals.\n".encode('utf-8'))
            client_socket.sendall(options.encode('utf-8'))


    def search_recitals(self, client_socket, options):
        try:
            search_name = "Search name: "
            client_socket.sendall(search_name.encode('utf-8'))
            user_input2 = client_socket.recv(1024).strip().decode('utf-8')
            parts = user_input2.split()
            search_term = parts[0]
            page = int(parts[1]) if len(parts) > 1 else 1
            per_page = int(parts[2]) if len(parts) > 2 else 10
            recitals, total = services.search_recitals(search_term, page=page, per_page=per_page)
            table_header = "ID | Artist | Date | Venue | Link \n"
            table_rows = []
            for recital in recitals:
                date = recital.date.strftime('%Y-%m-%d') if recital.date else ''
                row = f"{recital.id} | {recital.artist} | {date} | {recital.venue} | {recital.link}\n"
                table_rows.append(row)
            table = table_header + ''.join(table_rows)
            client_socket.sendall((table + '\n\n\n' + options).encode('utf-8'))
        except Exception as e:
            print(f"Error searching recitals: {e}")
            client_socket.sendall("Error searching recitals.\n".encode('utf-8'))
            client_socket.sendall(options.encode('utf-8'))


    def edit_configurations(self, client_socket, options):
        try:
            client_socket.sendall("Edit configurations feature is not yet implemented.\n".encode('utf-8'))
            client_socket.sendall(options.encode('utf-8'))
        except Exception as e:
            print(f"Error editing configurations: {e}")
            client_socket.sendall("Error editing configurations.\n".encode('utf-8'))
            client_socket.sendall(options.encode('utf-8'))


    def trigger_scraper_process(self, client_socket, options):
        try:
            manager = save_recitals.ScraperManager()
            manager.run()
            client_socket.sendall("Scraper triggered.\n".encode('utf-8'))
            client_socket.sendall(options.encode('utf-8'))
        except Exception as e:
            print(f"Error editing configurations: {e}")
            client_socket.sendall("Error editing configurations.\n".encode('utf-8'))
            client_socket.sendall(options.encode('utf-8'))

   