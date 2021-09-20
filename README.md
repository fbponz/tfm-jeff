## tfm-jeff-edem
<img align="center" width="270" height="136" src="http://www.gepacv.org/wp-content/uploads/2017/01/EDEM-Logo--540x272.png">

* [Jorge Camañez](https://github.com/jcamcre)
* [Miguel Ángel Parra](https://github.com/MiguelAngelPR)
* [Santiago Jacobo](https://www.linkedin.com/in/santiagojacobo/)
* [Borja Ponz](https://github.com/fbponz)

TFM, location inteligence

## Objetivo 
Ser capaces de determinar el area de captación de clientes, teniendo solo referencia en una localización concreta.

Para ello se ha optado la utilización de un huff model. Donde se calculara la probabilidad de atraer clientes de unas zonas determinas. 

El modelo huff (https://en.wikipedia.org/wiki/Huff_model), donde las variables:

+ Aj es el atractivo de medido de la tienda j
+ Dij es la distancia entre el consumidor i y la tienda j
+ alpha es el parámetro de atractivo.
+ beta es el parámetro de decaer por distancia.
+ N es el total de tiendas, incluyendo la tienda j.

Para el calculo de la distancia (Dij), se va a utilizar la formula de semiverseno: https://es.wikipedia.org/wiki/Fórmula_del_semiverseno

Para el calculo de atracción se va a utilizar la siguiente formula:
Atracción tienda = ((Sum(Puntos de Interes)/ Num_Secciones_Censales)-(lavanderias/Num_Secciones_Censales)+(total_poblacion/Num_Secciones_Censales))

### Apartados a visitar:
+ [Datasets](/datasets)
+ [Scripts](/scripts)
+ [API Keys](/keys)

## POC

Para utilizar el POC, debemos cargar el [notebook](scripts/TFM_POC.ipynb)

Primero se indica la calle sobre la cual se desea calcular el trade catchment area en la siguiente casilla
<img align="center" width="532" height="42" src="/img/Trade_Catchment_Area_Street_Name.png">

Se ejecutan todas las casillas y se obtiene un resultado como el siguiente 

<img align="center" width="1253" height="752" src="/img/Trade_Catchment_Area.png">

Si se pincha en uno de los marcadores o el circulo que indica la localización de la nueva tienda aparece el siguiente pop-up donde contiene el nombré de la tienda para poder analizar.
<img align="center" width="1253" height="752" src="/img/Trade_Catchment_Area_Detalle.png">


## Futuras Mejoras:

+ Modificar el calculo de la distancia mediante la formula de haversine a un método que tengan en cuenta las barreras arquitectónicas.
+ Dividir el campo puntos de interes y ponderarlo por tipos y sub-tipos.



