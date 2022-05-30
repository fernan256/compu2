# Rot13 con threading [th_rot13]

Escribir un programa que genere dos hilos utilizando threading.

Uno de los hilos deberá leer desde stdin texto introducido por el usuario, y deberá escribirlo en un mecanismo IPC (*).

El segundo hijo deberá leer desde dicho mecanismo IPC el contenido de texto, lo encriptará utilizando el algoritmo ROT13, y lo almacenará en una cola de mensajes (queue).

El primer hijo deberá leer desde dicha cola de mensajes y mostrar el contenido cifrado por pantalla.

(*) Verificar si el uso de os.pipe(), named pipes, o multiprocessing.Pipe() son thread-safe, caso contrario usar Queue.
