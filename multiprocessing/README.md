# Rot13 con multiprocessing [mp_rot13]

Escribir un programa que genere dos hijos utilizando multiprocessing.

Uno de los hijos debera leer desde stdin texto introducido por el usuario, y debera escribirlo en un pipe (multiprocessing)

El segundo hijo debera leer desde el pipe el contenido de texto, lo encriptara utilizando el algoritmo ROT13, y lo almacenara en una cola de mensajes (multiprocessing).

El primer hijo debera leer dicha cola de mensaje y mostrar el contenido cifrado por pantalla.
