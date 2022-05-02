# Ejercicio Inversor de caracteres - [mmap_sig]

Escribir un programa que reciba por argumento la opción -f acompañada de un path_file.
Etapa 1:

El programa deberá crear un segmento de memoria compartida anónima, y generar dos hijos: H1 y H2

El H1 leerá desde el stdin línea por línea lo que ingrese el usuario.

Cada vez que el usuario ingrese una línea, H1 la almacenará en el segmento de memoria compartida, y enviará la señal USR1 al proceso padre.

El proceso padre, en el momento en que reciba la señal USR1 deberá mostrar por pantalla el contenido de la línea ingresada por el H1 en la memoria compartida, y deberá notificar al H2 usando la señal USR1.

El H2 al recibir la señal USR1 leerá la línea desde la memoria compartida la línea, y la almacenará en mayúsculas en el archivo pasado por argumento (path_file).
Etapa 2:

Cuando el usuario introduzca "bye" por terminal, el hijo H1 enviará la señal USR2 al padre indicando que va a terminar, y terminará.
El padre, al recibir la señal USR2 la enviará al H2, que al recibirla terminará también.
El padre esperará a que ambos hijos hayan terminado, y terminará también.