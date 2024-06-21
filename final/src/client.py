import getpass
import socket
import signal
import sys
import os
import argparse
import select

class Client:
    def __init__(self, server_address, server_port, address_family):
        self.server_address = server_address
        self.server_port = server_port
        self.address_family = address_family

        self.client_socket = socket.socket(self.address_family, socket.SOCK_STREAM)
        self.client_running = True
        self.password_prompt = False
        self.new_password_prompt = False

    def signal_handler(self, sig, frame):
        print("Ctrl+C pressed. Disconnecting from server.")
        self.client_running = False
        self.client_socket.close()
        os._exit(0)

    def receive_message(self):
        try:
            response = self.client_socket.recv(2048).decode('utf-8')
            if response:
                print(f"Server Response: {response}")
                if "SERVER_SHUTDOWN" in response:
                    print("Server is shutting down. Goodbye!")
                    self.client_running = False
                    os._exit(0)
                if "Enter password:" in response:
                    self.password_prompt = True
                elif "Enter new password:" in response:
                    self.new_password_prompt = True
                else:
                    self.password_prompt = False

        except (ConnectionError, BrokenPipeError):
            print("Server disconnected unexpectedly.")
            self.client_running = False

    def send_command_to_server(self, command):
        try:
            self.client_socket.sendall(command.encode('utf-8'))

        except (ConnectionError, BrokenPipeError):
            print("Server disconnected unexpectedly.")
            self.client_socket.close()
            self.client_running = False

        except Exception as e:
            print(f"Error communicating with the server: {e}")

    def connect(self):
        try:
            self.client_socket.connect((self.server_address, self.server_port))
            print("Connected to the server. You can now login or signup.")
            return True
        except Exception as e:
            print(f"Error connecting to the server: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description="Client for IPv4 and IPv6 server.")
    parser.add_argument('protocol', choices=['ipv4', 'ipv6'], help="Specify whether to use IPv4 or IPv6.")
    parser.add_argument('server_address', help="The server address to connect to.")
    parser.add_argument('server_port', type=int, help="The server port to connect to.")
    args = parser.parse_args()

    if args.protocol == 'ipv4':
        address_family = socket.AF_INET
    elif args.protocol == 'ipv6':
        address_family = socket.AF_INET6

    client = Client(args.server_address, args.server_port, address_family)

    signal.signal(signal.SIGINT, client.signal_handler)

    if client.connect():
        while client.client_running:
            read_sockets, _, _ = select.select([client.client_socket, sys.stdin], [], [])

            for sock in read_sockets:
                if sock == client.client_socket:
                    client.receive_message()
                    if client.password_prompt:
                        password = getpass.getpass("Enter password: ")
                        client.send_command_to_server(password)
                        client.password_prompt = False
                    if client.new_password_prompt:
                        new_password = getpass.getpass("Enter new password: ")
                        client.send_command_to_server(new_password)
                        client.new_password_prompt = False
                elif sock == sys.stdin:
                    user_input = input()
                    if user_input.lower() == 'exit':
                        client.client_running = False
                        break
                    client.send_command_to_server(user_input)

        client.client_socket.close()

if __name__ == "__main__":
    main()
