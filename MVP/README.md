## tfm-jeff-edem
<img align="center" width="270" height="136" src="http://www.gepacv.org/wp-content/uploads/2017/01/EDEM-Logo--540x272.png">

## MVP
En está sección vamos a describir los pasos para poder en funcionamiento las diferentes partes del MVP. Por un lado tenemos el dashboard y por otro tenemos la arquitectura cloud que gastaremos para el procesado y generación de la salida.

### Arquitectura
La arquitectura propuesta para la solución se ha diseñado para ser implementada y puesta en producción en Google Cloud Platform.
Consta de dos partes principales una el Dashboard y el Backend.
<img align="center" width="714" height="371" src="/img/gcp_architecture.png">

### Dashboard

El dashboard puede ejecutar tanto en local o en una instancia de maquina virtual en GCP.

Para correrlo en local necesitamos tener instalado [Docker](https://www.docker.com) , nos descargamos el repositorio y nos dirigimos a la carpeta [App](../App) y ejecutamos las siguientes instrucciones.

    git clone https://github.com/fbponz/tfm-jeff.git
    cd tfm-jeff/App
    docker build -t dashboard .

    docker run -p 80:8080 dashboard
Una vez ejecutadas las instrucciones anteriores, podemos dirigirnos con nuestro navegador a la dirección http:\\localhost:80, esto nos abria el dashboard pero antes que nada debemos preparar t

### Backend

Lo primero que se debe hacer es crear una cuenta en Google Cloud Platform. Una vez se dispone de cuenta nos dirigimos al siguiente [Link](https://cloud.google.com/resource-manager/docs/creating-managing-projects) Para crear el proyecto necesario.

Una vez tenemos creado el proyecto el siguiente paso es habilitar las siguientes APIs:
  + Cloud Functions
  + Cloud Storage
  + Big query
  + Compute Engine
Estas son las principales API que se van a gastar para desplegar la arquitectura. Una vez tenemos la siguientes API habilitadas empezaremos creando un Bucket para nuestro proyecto.

      Descripción general
        Tipo de ubicación: Region
        Ubicación: europe-west6 (Zúrich)
        Clase de almacenamiento predeterminada: Standard
      Permisos
        Control de acceso: Uniforme
      Acceso público: No público
      Protección
        Tipo de encriptación:Google-managed key 
        
Una vez tenemos el bucket creado, vamos a proceder a subir todos los ficheros .csv en la carpeta [csv_cloud_storage](csv_cloud_storage/)

bigquery creamos un conjunto de datos en nuestro caso lo llamamos "TfmEdem", creamos la tablas por cada uno de los ficheros que tenemos el Cloud Storage y seleccionamos importar desde Cloud storage.

Cuando tenemos importados los datos debemos crear una cloud function cargando el codigo disponible en la [carpeta](/Cloud_Function) y modificamos las querys(Buscar la cadena de texto {TuProyecto}.{NombreBigQuery}, para agilizar los cambios) para que apunten a nuestro proyecto y las tablas de bigquery ademas debemos añadir también la clave de la API de [Mapbox](../keys)({Clave de Mapbox API}).

### Test solución
Una vez tenemos ambas partes funcionando, nos dirigimos a la dirección http://localhost:80. 

Vamos al test input, y ponemos la siguiente dirección la dirección con el siguiente formato

  {Calle/Avenida} Cuenca 15, Valencia, Valencia

Por el momento sistema funciona con las secciones censales de la ciudad de valencia.
<img align="center" width="1376" height="984" src="/img/Dashboard.png">
 
