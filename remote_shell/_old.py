import socket, os, sys, argparse, time, threading

def th_server(sock):
    print("Launching thread...")
    while True:
        msg = sock.recv(1024)
        print("Recibido: %s" % msg.decode())
        msg = "Ok"+" \r\n"
        sock.send(msg.encode("ascii"))
        #clientsocket.close()

def main(args):

  print(args)
  serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

  host = "localhost"
  port = int(args.port)
  print(host,port)

  serversocket.bind((host,port))

  serversocket.listen(5)

  while True:
    if args.proc:
      clientsocket,addr = serversocket.accept()

      print("Tengo conexion, desde %s" % str(addr))

      msg = 'Gracias por conectarse' + "\r\n"

      clientsocket.send(msg.encode('ascii'))

      child_pid = os.fork()

      if not child_pid:
        while True:
          msg = clientsocket.resv(1024)
          print("Recibido: %s" % msg.decode())
          msg = "ok" + " \r\n"
          clientsocket.send(msg.encode("ascii"))

    elif args.thread:
      clientsocket,addr = serversocket.accept()

      print("Got a connection from %s" % str(addr))

      msg = 'Thank you for connecting'+ "\r\n"
      clientsocket.send(msg.encode('ascii'))
      th = threading.Thread(target=th_server, args=(clientsocket,))
      th.start()

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-p", '--port', required=True,
                        help='Puerto de conexion')
	parser.add_argument("-cp", '--proc',
                      help='Nuevo proceso para nueva conexion',
                      action='store_true')
	parser.add_argument('-ct', '--thread',
                      help='Nuevo hilo para nueva conexion',
                      action='store_true')
	args = parser.parse_args()
	main(args)