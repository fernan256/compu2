import math
import socketserver
import sys
import signal
import threading
import time

from utils import common_utils 
from app.services import services
from scrapers import save_recitals


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
                prompt = "Que quiere realizar LOGIN or SIGNUP? ('exit' para Salir): "
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
        client_socket.sendall("Username: ".encode('utf-8'))
        username = client_socket.recv(1024).strip().decode('utf-8')

        client_socket.sendall("Password: ".encode('utf-8'))
        password = client_socket.recv(1024).strip().decode('utf-8')

        log_message = f"Login method"
        common_utils.log_queue.put(log_message)

        try:
            user = services.authenticate_user(username, password)
            if user:
                response = "Login correcto.\n"
                client_socket.sendall(response.encode('utf-8'))

                options = ("Seleccionar una opcion:\n"
                            "1. Listar Recitales Guardados\n"
                            "2. Buscar en paginas\n"
                            # "3. Editar Configuraciones de Usuario\n"
                            "3. Agregar a Favoritos\n"
                            "4. Eliminar de Favoritos\n"
                            "5. Actualizar recitales\n"
                            "'exit' para logout.\n")
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
                        self.add_to_favs(client_socket, options, user.id)
                    elif user_input == '5':
                        self.remove_from_favs(client_socket, options, user.id)
                    elif user_input == '6':
                        self.trigger_scraper_process(client_socket, options)
                    else:
                        client_socket.sendall("Comando no reconocido. Tratar nuevamente.".encode('utf-8'))
                        client_socket.sendall(options.encode('utf-8'))
            else:
                response = "Login falo. Saliendo del thread. \n"
                client_socket.sendall(response.encode('utf-8'))
        except Exception as e:
            print(f"Error connecting: {e}")
            response = "No se pudo conectar a la base de datos. Saliendo del thread. \n"
            client_socket.sendall(response.encode('utf-8'))


    def handle_signup(self, client_socket):
        client_socket.sendall("Nuevo Usuario: ".encode('utf-8'))
        new_username = client_socket.recv(1024).strip().decode('utf-8')

        client_socket.sendall("Nueva Contraseña: ".encode('utf-8'))
        new_password = client_socket.recv(1024).strip().decode('utf-8')

        client_socket.sendall("Nuevo Email: ".encode('utf-8'))
        new_email = client_socket.recv(1024).strip().decode('utf-8')

        try:
            services.create_user(new_username, new_password, new_email)

        except Exception as e:
            print(f"Error connecting: {e}")
            response = f"{e}. Saliendo del thread."
            client_socket.sendall(response.encode('utf-8'))


    def list_recitals(self, client_socket, options, user_id):
        try:
            page_option = "Indicar Pagina y Cantidad de elementos por pagina (opcional) ej (1 10): "
            client_socket.sendall(page_option.encode('utf-8'))
            page_per_page = client_socket.recv(1024).strip().decode('utf-8')
            parts = page_per_page.split()
            page = int(parts[0])
            per_page = int(parts[1]) if len(parts) > 1 else 10
            recitals, favorites, total = services.get_recitals(user_id, page=page, per_page=per_page)
            recitals_table = common_utils.get_table_rows(recitals)
            if favorites:
                recitals_table = recitals_table + ''.join(f'Favoritos: \n {common_utils.get_table_rows(favorites)}')
            response = recitals_table + ''.join(f'Paginas: {math.ceil(total/per_page)}, Total: {total}')
            client_socket.sendall((response + '\n\n\n' + options).encode('utf-8'))
        except Exception as e:
            print(f"Error listing recitals: {e}")
            client_socket.sendall("Error listing recitals.\n".encode('utf-8'))
            client_socket.sendall(options.encode('utf-8'))


    def search_recitals(self, client_socket, options):
        try:
            search_name = "Buscador: "
            client_socket.sendall(search_name.encode('utf-8'))
            page_per_page = client_socket.recv(1024).strip().decode('utf-8')
            parts = page_per_page.split()
            search_term = parts[0]
            page = int(parts[1]) if len(parts) > 1 else 1
            per_page = int(parts[2]) if len(parts) > 2 else 10
            recitals, total = services.search_recitals(search_term, page=page, per_page=per_page)
            recitals_table = common_utils.get_table_rows(recitals)
            response = recitals_table + ''.join(f'\nPaginas: {math.ceil(total/per_page)}, Total: {total}')
            client_socket.sendall((response + '\n\n\n' + options).encode('utf-8'))
        except Exception as e:
            print(f"Error searching recitals: {e}")
            client_socket.sendall("Error searching recitals.\n".encode('utf-8'))
            client_socket.sendall(options.encode('utf-8'))


    def add_to_favs(self, client_socket, options, user_id):
        try:
            search_name = "Id Recital: "
            client_socket.sendall(search_name.encode('utf-8'))
            id_recital = client_socket.recv(1024).strip().decode('utf-8')
            parts = id_recital.split()
            recitals = services.add_favorite(user_id, parts[0])
            if recitals:
                client_socket.sendall((f"Recital con ID:{parts[0]} Agregado a Favoritos" + '\n\n\n' + options).encode('utf-8'))
        except Exception as e:
            print(f"Error searching recitals: {e}")
            client_socket.sendall("Error searching recitals.\n".encode('utf-8'))
            client_socket.sendall(options.encode('utf-8'))


    def remove_from_favs(self, client_socket, options, user_id):
        try:
            search_name = "Id Recital: "
            client_socket.sendall(search_name.encode('utf-8'))
            id_recital = client_socket.recv(1024).strip().decode('utf-8')
            parts = id_recital.split()
            recitals = services.remove_favorite(user_id, parts[0])
            if recitals:
                client_socket.sendall((f"Recital con ID:{parts[0]} Eliminado de Favoritos" + '\n\n\n' + options).encode('utf-8'))
        except Exception as e:
            print(f"Error searching recitals: {e}")
            client_socket.sendall("Error searching recitals.\n".encode('utf-8'))
            client_socket.sendall(options.encode('utf-8'))


    # def edit_configurations(self, client_socket, options):
    #     try:
    #         client_socket.sendall("Edit configurations feature is not yet implemented.\n".encode('utf-8'))
    #         client_socket.sendall(options.encode('utf-8'))
    #     except Exception as e:
    #         print(f"Error editing configurations: {e}")
    #         client_socket.sendall("Error editing configurations.\n".encode('utf-8'))
    #         client_socket.sendall(options.encode('utf-8'))


    def trigger_scraper_process(self, client_socket, options):
        try:
            services.update_recitals()
            client_socket.sendall("Scraper triggered.\n".encode('utf-8'))
            client_socket.sendall(options.encode('utf-8'))
        except Exception as e:
            print(f"Error editing configurations: {e}")
            client_socket.sendall("Error editing configurations.\n".encode('utf-8'))
            client_socket.sendall(options.encode('utf-8'))

   