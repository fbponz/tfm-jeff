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
## Futuras Mejoras:

+ Modificar el calculo de la distancia mediante la formula de haversine a un método que tengan en cuenta las barreras arquitectónicas.
+ Dividir el campo puntos de interes y ponderarlo por tipos y sub-tipos.



