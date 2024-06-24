# Final Computación 2

## Scraper de paginas web

### Informacion del proyecto

https://github.com/fernan256/compu2/blob/feature/update_documentation/final/docs/descripcion.md

## Como usar el programa

### Componentes

Docker
python
virtualenv

## Requisitos
### Componenetes necesarios
Docker instalado
Python 3.7+
### Realizar lo siguiente para poder correr ipv6 desde un contenedor
Editar el archivo /etc/docker/daemon.json, en caso de que no exista crearlo con el siguiente comando
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
clear && python scrapers/save_recitals.py
```


## Comandos utiles

```
docker inspect -f '{{range .NetworkSettings.Networks}}{{.GlobalIPv6Address}}{{end}}' final-python-1
```

## Links utiles

https://docs.docker.com/config/daemon/ipv6/
