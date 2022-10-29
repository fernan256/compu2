Escriba un programa cliente/servidor en python que permita ejecutar comandos GNU/Linux en una computadora remota.

Técnicamente, se deberá ejecutar un código servidor en un equipo “administrado”, y programar un cliente (administrador) que permita conectarse al servidor mediante sockets STREAM.

El cliente deberá darle al usuario un prompt en el que pueda ejecutar comandos de la shell.

Esos comandos serán enviados al servidor, el servidor los ejecutará, y retornará al cliente:

    la salida estándar resultante de la ejecución del comando
    la salida de error resultante de la ejecución del comando.

El cliente mostrará en su consola local el resultado de ejecución del comando remoto, ya sea que se haya realizado correctamente o no, anteponiendo un OK o un ERROR según corresponda.

El servidor debe atender solicitudes utilizando sockets de alto nivel con serversocket.

El servidor debe poder recibir las siguientes opciones:

    -p <port>: puerto donde va a atender el servidor.
    -c p | t : modo de concurrencia. Si la opción es "-c p" el servidor generará un nuevo proceso al recibir conexiones nuevas. Si la opción es "-c t" generará hilos nuevos.

El cliente debe poder recibir las siguientes opciones:

    -h <host> : dirección IP o nombre del servidor al que conectarse.
    -p <port> : número de puerto del servidor.

Para leer estos argumentos se recomienda usar módulos como argparse o click.

Ejemplo de ejecución del cliente (la salida de los comandos corresponden a la ejecución en el equipo remoto.

diego@cryptos$ python3 ejecutor_cliente.py -h 127.0.0.1 -p 2222
> pwd
OK
/home/diego
> ls -l /home
OK
drwxr-xr-x 158 diego diego 20480 May 26 18:57 diego
drwx------   2 root  root  16384 May 28  2014 lost+found
drwxr-xr-x   6 andy  andy   4096 Jun  4  2015 user
> ls /cualquiera
ERROR
ls: cannot access '/cualquiera': No such file or directory
>

Pista: puede usar la clase Popen del módulo subprocess para ejecutar un comando y capturar las salidas