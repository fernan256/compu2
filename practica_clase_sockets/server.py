import socket, sys
import threading


def thread(socket):
    while True:
        datos = socket.recv(1024)
        datos_to_upper = datos.decode('UTF-8').upper()
        data_to_send = f"server: {datos_to_upper}"
        if datos.decode('UTF-8') == "exit":
            print("Cliente saliendo")
            socket.send("by".encode("ascii"))
            clientsocket.close()
            break
        else:
            socket.send(data_to_send.encode("ascii"))
            print(f"Recibido de {addr}: {datos_to_upper}")


host = ""
port = 1556

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen(1)

while True:
    # establish a connection
    clientsocket,addr = sock.accept()

    print("Conexion de cliente %s" % str(addr))

    th = threading.Thread(target=thread, args=(clientsocket,))
    th.start()
