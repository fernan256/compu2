# Final Computación 2

## Scrapper de paginas web

### Resumen

#### El trabajo se basara en un sistema de scrapping de paginas de eventos (o cualquier pagina). Se realizará un procesado a la información que se obtenga y se permitirá guardar dicha información en una base de datos. Ademas se le dará la posibilidad al usuario de poder generar eventos en un calendario para dichos scrapping, ejemplo scrapear páginas web de recitales y poder guardar la info en una db y al mismo tiempo guardar el evento en un calendario.

#### Cuando se pase una web para scraping el sistema buscara primero en la base de datos si la misma no fue scrapeada anteriormente, en caso de existir en la base de datos, se escribira en el log.txt desde el hilo y se devolvera la informacion guardad.

#### Para la seguridad se agregara la posiblidad de crear/loguearse en una cuenta. Cada usuario podra crear su cuenta y loguearse.

#### Contara con una pequenia interfaz de usuario en la cual se mostrara la informacion scrapeada.

#### Cada usuario se conectara al servidor y podrá enviar 1 url para ser scrapeada, se le darán opciones al usuario para que pueda guardar en la base de datos, y colocar evento en el calendario. También podrá correr en linea de comandos con las opciones necesarias para scrapear, guardar y colocar evento en calendario.

#### Se utlizaran contenedores para tanto para las aplicaciones, como para la base de datos. Se utlizara docker compose para levantar el entorno.

### Hilos vs Subprocesos

#### Luego de un analisis entre ambas herramientas, para concurrencia, me decidi hilos, ya que estos son mas livianos en la creacion, comparten memoria y recursos y al ser mayormente operaciones de I/O, la utilizacion de hilos parece ser una mejor opcion que el uso de subprocesos. Al utilizar hilos podremos scrapear multiples pagainas al mismo tiempo, sin necesidad de bloquear la ejecucion del programa.

### Elementos que se usaran

#### Hilos para multiples conexiones de clientes de manera concurrente.
#### Mecanismos de IPC como queues.
#### Parseo de argumentos para linea de comandos.
#### Uso de contenedores para la aplicacion como para la base de datos.
#### Base de datos.
#### Interfaz de usuario

### Diagramas

![Diagrama_Trabajo_Final-Page-2 drawio](https://github.com/fernan256/compu2/assets/8095849/005de424-642a-4ebc-bd94-e130768220c8)

## Como usar el programa

### Componentes

#### Docker
#### python
#### virtualenv

## Requisitos
### Componenetes necesarios
#### Docker instalado
#### Python 3.7+
### Realizar lo siguiente para poder correr ipv6 desde un contenedor
#### Editar el archivo /etc/docker/daemon.json, en caso de que no exista crearlo con el siguiente comando
```
mkdir /etc/docker && touch /etc/docker/daemon.json
vim /etc/docker/daemon.json
```
#### Agregar las siguientes lineas
```
{
  "experimental": true,
  "ip6tables": true
}
```
#### Guardar el archivo y reiniciar el servicio de docker
```
sudo systemctl restart docker
```
#### Crear una nueva red IPV6 usando los siguientes comandos:
```
docker network create --ipv6 --subnet 2001:0DB8::/112 ip6net
```
#### Agregar el siguiente codigo a docker compose
```
networks:
  ip6net:
     enable_ipv6: true
     ipam:
       config:
         - subnet: 2001:0DB8::/112
```
#### Agregar la nueva red a nuestra aplicacion python

## Ejecucion de aplicacion y cliente

### Iniciar los contenedores con la aplicacion, base de datos, prometheus y grafana

#### En una terminal ejecutar el siguiente comando:

```
clear && docker compose build \
    --build-arg HOST_IPV4='0.0.0.0' \
    --build-arg HTTP_PORT_IPV4=8082 \
    --build-arg COMMAND_LINE_PORT_IPV4=9092 \
    --build-arg HOST_IPV6='::' \
    --build-arg HTTP_PORT_IPV6=8083 \
    --build-arg COMMAND_LINE_PORT_IPV6=9093 \
    --build-arg LOG_FILE=output.log \
    && docker compose up
```

### Inicializar la base de datos
#### Conectarse al contenedor de python en modo bash y ejecutar

```
docker exec -it final-python-1 bash

python -m init_db.py 
```

#### Al cual se le pueden pasar los siguientes comands:
##### HOST_IPV4
##### HTTP_PORT_IPV4
##### COMMAND_LINE_PORT_IPV4
##### HOST_IPV6
##### HTTP_PORT_IPV6
##### COMMAND_LINE_PORT_IPV6
##### LOG_FILE=output.log

### Ejecutar cliente

#### Para el cliente de linea de comandos podemos correr los siguientes comandos:


##### Para IPV4
```
clear && python src/client.py ipv4 172.22.0.5 9092
```

##### Para IPV6
```
clear && python src/client.py ipv6 2001:db8::2 9093
```

## Para correr el scraper en forma local

### Hay que modificar el archivo save_recitals y agregar un main para poder ejecutar la funcion en cuenta se corra el archivo.

```
cd final/
pipenv shell
cd src/
export PYTHONPATH=$(pwd):$PYTHONPATH
clear && python scrappers/save_recitals.py
```


## Comandos utiles

```
docker inspect -f '{{range .NetworkSettings.Networks}}{{.GlobalIPv6Address}}{{end}}' final-python-1
```

## Links utiles

https://docs.docker.com/config/daemon/ipv6/
