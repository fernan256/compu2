import socket
import threading
import signal
import sys
import os

class Client:
    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_running = True

    def signal_handler(self, sig, frame):
        print("Ctrl+C pressed. Disconnecting from server.")
        self.client_running = False
        self.client_socket.close()
        os._exit(0)

    def receive_messages(self):
        while self.client_running:
            try:
                response = self.client_socket.recv(1024).decode('utf-8')
                if response:
                    print(f"Server Response: {response}")

                    # Check for a shutdown message from the server
                    if "Server is shutting down" in response:
                        print("Server is shutting down. Goodbye!")
                        self.client_running = False
                        break

            except (ConnectionError, BrokenPipeError):
                print("Server disconnected unexpectedly.")
                break
        sys.exit(0)

    def send_command_to_server(self, command):
        try:
            self.client_socket.sendall(command.encode('utf-8'))

        except (ConnectionError, BrokenPipeError):
            print("Server disconnected unexpectedly.")
            # Handle disconnection as needed (e.g., close the client socket, exit the client)
            self.client_socket.close()
            self.client_running = False
            sys.exit()

        except Exception as e:
            print(f"Error communicating with the server: {e}")

    def login(self, username, password):
        try:
            self.client_socket.connect((self.server_address, self.server_port))
            self.client_socket.sendall(f"LOGIN {username} {password}".encode('utf-8'))

            response = self.client_socket.recv(1024).decode('utf-8')
            print(f"Server Response: {response}")

            if "Login successful" in response:
                print("Login successful! You can now interact with the server.")

                # Start a thread to receive messages from the server
                receive_thread = threading.Thread(target=self.receive_messages)
                receive_thread.start()

                # Continue handling user input in a new thread
                while self.client_running:
                    user_input = input("Enter a command (or 'exit' to quit): ")
                    if user_input.lower() == 'exit':
                        break

                    input_thread = threading.Thread(target=self.send_command_to_server, args=(user_input,))
                    input_thread.start()
                    input_thread.join()

                # Wait for the receive thread to finish before exiting
                receive_thread.join()

            else:
                print("Login failed. Exiting...")

        except ConnectionError as ce:
            print(f"ConnectionError: {ce}")

        except Exception as e:
            print(f"Error communicating with the server: {e}")

    def signup(self, new_username, new_password, new_email):
        try:
            self.client_socket.connect((self.server_address, self.server_port))
            self.client_socket.sendall(f"SIGNUP {new_username} {new_password} {new_email}".encode('utf-8'))

            response = self.client_socket.recv(1024).decode('utf-8')
            print(f"Server Response: {response}")

        except ConnectionError as ce:
            print(f"ConnectionError: {ce}")

        except Exception as e:
            print(f"Error communicating with the server: {e}")

if __name__ == "__main__":
    # revisar el tema del puerto y address y arreglar el tema de desconxion
    server_address = "172.21.0.3"
    server_port = 9092

    client = Client(server_address, server_port)

    signal.signal(signal.SIGINT, client.signal_handler)  # Register signal handler for Ctrl+C

    print("1. Login")
    print("2. Signup")

    choice = input("Enter your choice: ")

    if choice == '1':
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        client.login(username, password)

    elif choice == '2':
        new_username = input("Enter a new username: ")
        new_password = input("Enter a new password: ")
        new_email = input("Enter a new email: ")
        client.signup(new_username, new_password, new_email)

    else:
        print("Invalid choice. Exiting...")
