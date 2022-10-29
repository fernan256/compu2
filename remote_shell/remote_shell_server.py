import socketserver, argparse, pickle
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


def remote_shell(msg_client):
    command = sp.Popen(msg_client, stdout=sp.PIPE, stderr=sp.PIPE, shell=True, universal_newlines=True, bufsize= 10000)
    output, error = command.communicate()

    return {"output": output, "error": error}


def execute_p_socket(args):
    host = ""
    port = args.p
    socketserver.TCPServer.allow_reuse_address = True
    server = ForkedTCPServer((host,port), TcpHandler)
    server.serve_forever()


def execute_t_socket(args):
    host = ""
    port = args.p
    socketserver.TCPServer.allow_reuse_address = True
    with ThreadedTCPServer((host,port), TcpHandler) as server:
        server.serve_forever()


def main(args):
    if args.c == "p":
        execute_p_socket(args)
    else:
        execute_t_socket(args)
   

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", type=int, required=True, help="Puerto")
    parser.add_argument("-c", type=str, required=True, help="Concurrencia", choices=["p", "t"])
    args = parser.parse_args()
    main(args)