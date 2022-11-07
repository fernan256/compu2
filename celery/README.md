# TP Celery

## Realizar un programa en python que reciba por argumentos:

    -f /ruta/al/archivo_matriz.txt
    -c funcion_calculo

El programa deberá leer una matriz almacenada en el archivo de texto pasado por argumento -f, y deberá calcular la funcion_calculo para cada uno de sus elementos.

Para aumentar la performance, el programa utilizará un Celery, que recibirá mediante una cola de mensajes Redis, cada una de las tareas a ejecutar.

La funcion_calculo, modelada como tareas de Celery, podrá ser una de las siguientes:

    raiz: calcula la raíz cuadrada del elemento.
    pot: calcula la potencia del elemento elevado a si mismo.
    log: calcula el logaritmo decimal de cada elemento.

## Ejemplo de uso:

Suponiendo que el archivo /tmp/matriz.txt tenga este contenido:

1, 2, 3

4, 5, 6

python3 calculo_matriz -f /tmp/matriz.txt -c pot

1, 4, 9

16, 25, 36

## Pasos para ejecutar:
### Ejecutar redis en una terminal:

```bash
docker run --rm -p 6379:6379 redis
```
### Ejecutar Celery:
```bash
celery -A task worker --loglevel=INFO -c4
```

### Ejecutar programa para calcular matriz
```bash
python calculo_matricial.py -f ./matriz.txt -c log
```