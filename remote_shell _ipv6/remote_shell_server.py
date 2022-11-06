import socketserver, argparse, pickle, socket, threading, os
import subprocess as sp


class TcpHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print(f"Cliente {self.client_address} conectado.")

        while True:
            msg_client = self.request.recv(1024)
            msg_client = pickle.loads(msg_client)

            if msg_client == "exit":
                print(f"Client {self.client_address} saliendo.")
                self.request.sendall(pickle.dumps("By by"))
                break
            else:
                msg_client_dic = remote_shell(msg_client)
                msg_client_dic = pickle.dumps(msg_client_dic)
                self.request.sendall(msg_client_dic)


class ForkedTCPServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class ForkedTCPServerIPV6(socketserver.ForkingMixIn, socketserver.TCPServer):
    address_family = socket.AF_INET6
    pass


class ThreadedTCPServerIPV6(socketserver.ThreadingMixIn, socketserver.TCPServer):
    address_family = socket.AF_INET6
    pass


def remote_shell(msg_client):
    command = sp.Popen(msg_client, stdout=sp.PIPE, stderr=sp.PIPE, shell=True, universal_newlines=True, bufsize= 10000)
    output, error = command.communicate()

    return {"output": output, "error": error}


def execute_p_socket(args, dir):
    host = ""
    port = args.p
    socketserver.TCPServer.allow_reuse_address = True
    if dir[0] == socket.AF_INET: 
        print("ipv4")
        server = ForkedTCPServer((host,port), TcpHandler)
        server.serve_forever()
    elif dir[0] == socket.AF_INET6:
        print("ipv6")
        server = ForkedTCPServerIPV6((host,port), TcpHandler)
        server.serve_forever()


def execute_t_socket(args, dir):
    host = ""
    port = args.p
    socketserver.TCPServer.allow_reuse_address = True
    if dir[0] == socket.AF_INET: 
        print("ipv4")
        with ThreadedTCPServer((host,port), TcpHandler) as server:
            server.serve_forever()
    elif dir[0] == socket.AF_INET6:
        print("ipv6")
        with ThreadedTCPServerIPV6((host,port), TcpHandler) as server:
            server.serve_forever()
    

def services(args, dir):
    if args.c == "p":
        execute_p_socket(args, dir)
    else:
        execute_t_socket(args, dir)
   

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", type=int, required=True, help="Puerto")
    parser.add_argument("-c", type=str, required=True, help="Concurrencia", choices=["p", "t"])
    args = parser.parse_args()
    addrs = socket.getaddrinfo("localhost", args.p, socket.AF_UNSPEC, socket.SOCK_STREAM)
    hilo = []

    for dir in addrs:
        hilo.append(threading.Thread(target=services, args=(args, dir)))

    for h in hilo:
        h.start()