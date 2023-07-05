# Final Computación 2

## Scrapper de paginas web

### Resumen

#### El trabajo se basara en un sistema de scrapping de paginas de eventos (o cualquier pagina). Se realizará un procesado a la información que se obtenga y se permitirá guardar dicha información en una base de datos. Ademas se le dará la posibilidad al usuario de poder generar eventos en un calendario para dichos scrapping, ejemplo scrapear páginas web de recitales y poder guardar la info en una db y al mismo tiempo guardar el evento en un calendario.

#### Cada usuario se conectara al servidor y podrá enviar 1 url para ser scrapeada, se le darán opciones al usuario para que pueda guardar en la base de datos, y colocar evento en el calendario. También podrá correr en linea de comandos con las opciones necesarias para scrapear, guardar y colocar evento en calendario.

#### Se utlizaran contenedores para tanto para las aplicaciones, como para la base de datos. Se utlizara docker compose para levantar el entorno.

### Elementos que se usaran

#### Sockets para multiples coneziones de clientes de manera concurrente.
#### Mecanismos de IPC como pipes.
#### Parseo de argumentos par linea de comandos.
#### Uso de contenedores para la aplicacion como para la base de datos.
#### Base de datos.

### Diagramas

![Image text](https://github.com/fernan256/compu2/tree/main/final/doc/Diagrama_Trabajo_Final.png)