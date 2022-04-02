# Ejercicio Fork

Escribir un programa en Python que reciba los siguientes argumentos por línea de comandos:
```bash
-n

-h

-v
```

El programa debe generar procesos hijos, y cada proceso calculará la suma de todos los números enteros pares entre 0 y su número de PID.

El programa deberá mostrar por pantalla:

```bash
PID – PPID : <suma_pares>
```

El proceso padre debe esperar a que todos sus hijos terminen.

La opción -h mostrará ayuda de uso, y la opción -v habilitará el modo verboso de la aplicación. El modo verboso debe mostrar, además de la suma, un mensaje al inicio y al final de la ejecución de cada proceso hijo, que indique su inicio y fin.

## Ejemplos 1:
```bash
./sumapares.py -n 2

32803 – 4658: 269009202

32800 – 4658: 268943600
```
## Ejemplos 2:
```bash
./sumapares.py -n 2 -v

Starting process 32800

Starting process 32803

Ending process 32803

32803 – 4658: 269009202

Ending process 32800

32800 – 4658: 268943600
```