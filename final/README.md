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

### Ejecucion de comandos

#### docker run --name=mysql_container -d mysql/mysql-server:latest
#### docker run --rm \
--detach \
--name=mysql_container \
--env="MYSQL_ROOT_PASSWORD=\password \
--publish 3306:3306 \
--volume=/storage/docker/mysql-data:/var/lib/mysql \

#### python src/main_flask.py --host localhost --http_port 8082 --command_line_port 9092 --log_file src/output.txt