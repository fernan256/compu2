# Final Computación 2

## Scraper de paginas web

### Informacion del proyecto

https://github.com/fernan256/compu2/blob/feature/update_documentation/final/docs/descripcion.md

## Como usar el programa

### Componenetes

* Docker instalado
* Python 3.7+

### Instalación

#### Base de datos

Crear un archivo .env en la raíz del proyecto con la siguiente información

```
MYSQL_ROOT_PASSWORD='<su_contraseña>'
```

##### NOTA: Evitar usar @ en las contraseñas de mysql

#### Realizar lo siguiente para poder correr ipv6 desde un contenedor

Editar el archivo /etc/docker/daemon.json, en caso de que no exista crearlo con el siguiente comando

```
mkdir /etc/docker && touch /etc/docker/daemon.json
vim /etc/docker/daemon.json
```

Agregar las siguientes lineas:

```
{
  "experimental": true,
  "ip6tables": true
}
```

Guardar el archivo y reiniciar el servicio de docker:

```
sudo systemctl restart docker
```

Crear una nueva red IPV6 usando los siguientes comandos:

```
docker network create --ipv6 --subnet 2001:0DB8::/112 ip6net
```

Agregar el siguiente codigo a docker compose:

```
networks:
  ip6net:
     enable_ipv6: true
     ipam:
       config:
         - subnet: 2001:0DB8::/112
```

Agregar la nueva red a nuestra aplicacion python:

```
  python:
    build:
      context: .
      dockerfile: Dockerfile
    restart: always
    volumes:
      - ./src:/app
    depends_on:
      - db
    ports:
      - "8082:8082"
      - "9092:9092"
      - "8083:8083"
      - "9093:9093"
    networks:
      - main-network
      - ip6net
```

#### Iniciar los contenedores con la aplicacion, base de datos, prometheus y grafana

Crear un archivo .env dentro de la carpeta src/ con la siguiente información

```
DB_USERNAME='root'
DB_PASSWORD='pass'
DB_PORT=3306
DB_NAME='main_db'
SECRET_KEY='su_secret'
FLASK_SECRET_KEY='otro_secreto'
```

En una terminal ejecutar el siguiente comando:

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

Al cual se le pueden pasar los siguientes comands:

* HOST_IPV4='0.0.0.0'
* HTTP_PORT_IPV4=8082
* COMMAND_LINE_PORT_IPV4=9092
* HOST_IPV6='::'
* HTTP_PORT_IPV6=8083
* COMMAND_LINE_PORT_IPV6=9093
* LOG_FILE=output.log

#### Inicializar la base de datos

Conectarse al contenedor de python en modo bash y ejecutar

```
docker exec -it final-python-1 bash

python -m init_db.py 
```

#### Ejecutar clientes

Para el cliente de linea de comandos podemos correr los siguientes comandos:

##### Cliente CMD

###### IPv4

Obetener ipv4 de la aplicacion python

```
docker inspect -f '{{.NetworkSettings.Networks.final_main_network.IPAddress}}' final-python-1
```

Obtenemos la siguiente IPv4:

```
172.26.0.5
```

Donde la ip que necesitamos es la siguiente IPAddress

```
clear && python src/client.py ipv4 172.22.0.5 9092
```

###### IPv6

Obetener ipv6 de la aplicacion python

```
docker inspect -f '{{range .NetworkSettings.Networks}}{{.GlobalIPv6Address}}{{end}}' final-python-1
```

Obetenemos la siguiente IPv6:

```
2001:db8::2
```

```
clear && python src/client.py ipv6 2001:db8::2 9093
```

##### Cliente web

###### IPv4

http://localhost:8082

###### IPv6

Para acceder al pagina web debemos obtener la ip del contenedor que esta corriendo nuestra aplicacion, para ello usaremos el siguiente comando

```
docker inspect -f '{{range .NetworkSettings.Networks}}{{.GlobalIPv6Address}}{{end}}' final-python-1
```

Obetenemos la siguiente IPv6:

```
2001:db8::2
```

De donde podremos obtener tanto la ip para IPv6

IPv6: http://[2001:db8::2]:8083


## Para correr el scraper en forma local

### Hay que modificar el archivo save_recitals y agregar un main para poder ejecutar la funcion en cuenta se corra el archivo.

```
cd final/
pipenv shell
cd src/
export PYTHONPATH=$(pwd):$PYTHONPATH
clear && python scrapers/save_recitals.py
```

## Observabilidad

### Prometheus

Para acceder a las configuraciones de Prometheus usaremos la siguiente direccion

http://localhost:9090

### Grafana

Para acceder a Grafana usaremos la siguiente direccion

http://localhost:3000

Usuario y contraseña por defecto:

user: admin
pass: admin


## Comandos utiles

```
docker inspect -f '{{range .NetworkSettings.Networks}}{{.GlobalIPv6Address}}{{end}}' final-python-1
docker exec -it final-python-1 bash
ps -eLf | grep "python"
docker container ls
docker conatiner ls -a
docker inspect <contenedor>
docker images
docker volume ls
docker network ls
docker network inspect <network_name>
```

## Links utiles

https://docs.docker.com/config/daemon/ipv6/

# Troubleshoots

## Dbeaver database manager

Si tenes un error como el siguiente

```
“Public Key Retrieval is not allowed”
```

Here is the solution https://medium.com/@kiena/troubleshooting-dbeaver-public-key-retrieval-is-not-allowed-error-29f203d745c5

Go to the “Driver Properties” section. Locate the property named “allowPublicKeyRetrieval”. By default, it is set to “false”. Change the value of “allowPublicKeyRetrieval” to “TRUE”.

Imagen