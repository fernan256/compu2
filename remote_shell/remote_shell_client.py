import socket, pickle, argparse


def client(args):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
                    
    host = args.host
    port = int(args.port)

    s.connect((host, port))   

    while True:
        msg1 = input("> ")
        msg1 = pickle.dumps(msg1)
        s.send(msg1)

        msg2 = s.recv(10000)
        msg2 = pickle.loads(msg2)

        if pickle.loads(msg1).lower() == "exit":
            print(f"Server: {msg2}")

            s.close()
            exit()

        if msg2["error"] == "":
            print("Server OK: \n", msg2["output"])
        else:
            print("Server ERROR: \n", msg2["error"])


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-hs", '--host', required=True, help='host del sever')
  parser.add_argument("-p", '--port', required=True, help='Puerto de conexion')
  args = parser.parse_args()
  client(args)