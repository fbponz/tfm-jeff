## tfm-jeff-edem
<img align="center" width="270" height="136" src="http://www.gepacv.org/wp-content/uploads/2017/01/EDEM-Logo--540x272.png">

### Carpetas:

[TFM_POC.ipynb] es el notebook de la prueba de concepto planteada en este trabajo del TFM.
Para ejecutarlo debemos añadir/abrir los siguientes archivos.
+ mapboxkeys.csv
+ dataset_ine_valencia.csv
+ lavanderias.csv
+ poi_tratado.csv
+ seccensales.JSON

Una vez añadidos los siguientes ficheros podemos ejecutar el notebook, se recomienda modificar la casilla que contiene la dirección por la deseada. y seria suficiente con ejecutar todas las casillas, para obtener el mapa que determina la zona de atracción de clientes.



En la carpeta [Auxiliares](/Auxiliares):
+ TFM_ETL_Clean_data_and_create_dataset.ipynb -> Dataset INE.
+ TFM_ETL_DatasetGoogle.ipynb -> Transforma los datos obtenidos desde la API de google.
+ TFM_ETL_DatasetJeff_Seccensals.ipynb -> Transforma y añade secciones censales al dataset que nos proporciona la empresa.
+ TFM_ETL_Distancia_Entre_Dos_Puntos.ipynb -> Obtener distancias entre dos puntos utilizando la Mapbox.
+ TFM_ETL_DivideDataset.ipynb -> Divide el dataset que nos proporciona la empresa, y lo divide en los datos de valencia y de madrid.
+ TFM_ETL_Exploratory_Data_Analysis.ipynb -> EDA sobre los datos proporcionados por la empresa.
+ TFM_ETL_Get_GooglePlacesAPI.ipynb -> Obtiene los datos de la zona de valencia.
+ TFM_ETL_Request_Isochrones.ipynb -> Obtiene las isocronas gastando las API de mapbox.
+ TFM_TAC_Huff_Model.ipynb -> Implementación del modelo huff.
+ TFM_VSL_Folium_Barrios.ipynb -> Representación de los datos en un mapa.


En la carpeta [Cloud arquitecture](/Cloud_arquitecture):
+ TFM_Get_GooglePlacesAPI.ipynb -> Obtiene los datos de la zona de valencia.
+ TFM_ETL_TransformPOI.ipynb -> Transforma los datos obtenidos de la Google Places API.
+ TFM_Isochrone.ipynb -> Obtener las isocronas de Mapbox API.



