# Ejercicio Fork

Escribir un programa en Python que reciba los siguientes argumentos por línea de comandos:

```bash
-n <N>
-r <R>
-h
-f <ruta_archivo>
-v
```

El programa deberá abrir (crear si no existe) un archivo de texto cuyo path ha sido pasado por argumento con ```-f```.

El programa debe generar ```<N>``` procesos hijos. Cada proceso estará asociado a una letra del alfabeto (el primer proceso con la "A", el segundo con la "B", etc). Cada proceso almacenará en el archivo su letra ```<R>``` veces con un delay de un segundo entre escritura y escritura (realizar flush() luego de cada escritura).

El proceso padre debe esperar a que los hijos terminen, luego de lo cual deberá leer el contenido del archivo y mostrarlo por pantalla.

La opción ```-h``` mostrará ayuda. La opción ```-v``` activará el modo verboso, en el que se mostrará antes de escribir cada letra en el archivo: Proceso ```<PID>``` escribiendo letra ```'X'```.


## Ejemplos 1:
```bash
./escritores.py -n 3 -r 4 -f /tmp/letras.txt

ABCACBABCBAC
```
## Ejemplos 2:
```bash
./escritores.py -n 3 -r 5 -f /tmp/letras.txt -v

Proceso 401707 escribiendo letra 'A'
Proceso 401708 escribiendo letra 'B'
Proceso 401709 escribiendo letra 'C'
Proceso 401708 escribiendo letra 'B'
Proceso 401707 escribiendo letra 'A'
Proceso 401709 escribiendo letra 'C'
Proceso 401707 escribiendo letra 'A'
Proceso 401708 escribiendo letra 'B'
Proceso 401709 escribiendo letra 'C'
Proceso 401707 escribiendo letra 'A'
Proceso 401708 escribiendo letra 'B'
Proceso 401709 escribiendo letra 'C'
Proceso 401707 escribiendo letra 'A'
Proceso 401708 escribiendo letra 'B'
Proceso 401709 escribiendo letra 'C'
ABCBACABCABCABC
```