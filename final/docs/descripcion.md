# Final Computación 2

## Scrapper de paginas web

### Resumen

El trabajo se basara en un sistema de scrapping de paginas de eventos. Se realizará un procesado a la información que se obtenga y se permitirá guardar dicha información en una base de datos. El scraper 

Las paginas que se pueden scrapear son indihoy, livepass, songkick y tu entrada, se realizara el scraper particular para cada una de ellas. La forma en que el scraper funcionara sera el siguiente, se creara un servicio para scrapear que se podra dispara bajo demanda, el cual creara 1 hilo por cada scraper cada uno de ellos hara la tarea de scraper y luego a la hora de guardar en la base de datos, primero chequeara que el evento no exista en la db (buscar duplicados), en caso de que exista no hara nada y si no existe se guardar en la base de datos, lo otro sera verificar eventos pasados a los cuales se les pondra el flag de delete = true.

Para la seguridad se agregara la posiblidad de crear/loguearse en una cuenta. Cada usuario podra crear su cuenta y loguearse.

Se podra usar tando linea de comandos como una pagina web para ver los recitales guardados.

Contara con una pequeña interfaz de usuario en la cual se mostrara la informacion scrapeada.

Cada usuario se conectara al servidor y podrá listar eventos, agregar y eliminar de favoritos y ejecutar un proceso para actualizar recitales.

Se utlizaran contenedores tanto para las aplicaciones, como para la base de datos. Se utlizara docker compose para levantar el entorno.

Ademas se agregara un parte de observabilidad para conocer el estado del contenedor sabien memoria utilizada y cantidad de hilos creados.

### Hilos vs Subprocesos

Luego de un analisis entre ambas herramientas, para concurrencia, me decidi hilos, ya que estos son mas livianos en la creacion, comparten memoria y recursos y al ser mayormente operaciones de I/O, la utilizacion de hilos parece ser una mejor opcion que el uso de subprocesos. Al utilizar hilos podremos scrapear multiples pagainas al mismo tiempo, sin necesidad de bloquear la ejecucion del programa.

### Elementos que se usaran

Hilos para multiples conexiones de clientes de manera concurrente.
Mecanismos de IPC como queues.
Parseo de argumentos por linea de comandos.
Uso de contenedores para la aplicacion como para la base de datos.
Base de datos.
Interfaz de usuario.
Observabilidad.

### Diagramas

![diagrama-v2](https://github.com/fernan256/compu2/blob/main/final/docs/diagrama-v2.png)

### Links

https://drive.google.com/file/d/14v6VHwoDQnwm1dKRoGHeFsj6c2z5nM4e/view