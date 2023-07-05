Modificar el código de shell remota realizado con anterioridad ([serversocket]) para que atienda en todas las IP's del sistema operativo, independientemente de que se trate de IPv4 o IPv6.

Lance un thread para cada socket.

El servidor de shell debe mantener la concurrencia para atender a varios clientes, ya sea por procesos o hilos, dependiendo del parámetro pasado por argumento "-c".