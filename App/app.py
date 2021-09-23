
# Importamos las librerias
import pandas as pd
from pandas.core.frame import DataFrame
import numpy as np
import requests
from flask import Flask, request, jsonify, render_template, url_for
import pickle
import json
import random
import string
import time
import shapely
from shapely.geometry import shape, GeometryCollection, Point, Polygon
from shapely import wkt
import streamlit as st
import folium
from streamlit_folium import folium_static
import streamlit.components.v1 as components
import geopandas as gpd

@st.cache(allow_output_mutation=True)
def seccensales_data():
    with open('data/seccensales.JSON') as f: 
        seccensales_geojson = json.load(f)
    for idx in range(len(seccensales_geojson['features'])):
        seccensales_geojson['features'][idx]['properties']['coddistsec'] = int(seccensales_geojson['features'][idx]['properties']['coddistsec'])
    return seccensales_geojson

@st.cache
def dataset_ine_get():
    dtst_ine = pd.read_csv('data/dataset_ine_valencia.csv', sep=',', decimal='.')
    return dtst_ine


@st.cache(allow_output_mutation=True)
def test_output_date():
    with open('data_test/sample.json') as f: 
        api_request = json.load(f)
    df = pd.json_normalize(api_request['49'])
    data3 = json.loads(df['Prob_Huff'][0])
    df2 = pd.DataFrame.from_dict(data3, orient="index")
    dtst_poi_loc = []
    df_poi_location = pd.DataFrame(dtst_poi_loc, columns=[])
    for i in range(len(df['list_of_poi'][0])):
        df_poi_location = df_poi_location.append(pd.json_normalize(df['list_of_poi'][0][i]),ignore_index=True)
    return df, df2, df_poi_location

@st.cache
def get_api_output_date(street_name):
    r =requests.post('https://europe-west6-tfmedem.cloudfunctions.net/API_TFM', json={'street_name':street_name})
    json_object = json.dumps(r.json(), indent = 4)
    data = json.loads(json_object)
    df = pd.json_normalize(data['49'])
    data3 = json.loads(df['Prob_Huff'][0])
    df2 = pd.DataFrame.from_dict(data3, orient="index")
    dtst_poi_loc = []
    df_poi_location = pd.DataFrame(dtst_poi_loc, columns=[])
    for i in range(len(df['list_of_poi'][0])):
        df_poi_location = df_poi_location.append(pd.json_normalize(df['list_of_poi'][0][i]),ignore_index=True)
    return df, df2, df_poi_location

def obtener_secciones_censales_lavanderia(df):
    seccensales_list = []
    
    return seccensales_list

def card_db(string, value):
    card_html = """
    <style>
    .container {
        background-color: #ECECEC;
        text-align: center;
        user-select: none;
        font-size: 43px;
    }
    .card {
    }
    .h4 {
        background-color: #ECECEC;
        text-align: center;
        user-select: none;
        font-size: 43px;
    }
    .h5 {
        background-color: #ECECEC;
        text-align: center;
        user-select: none;
        font-size: 25px;
    }
    </style> 
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    <div class="card">
        <div class="container">
            <h4><b>"""+string+"""</b></h4> 
            <h5>"""+value+"""</h5> 
        </div>
    </div>
    """
    return card_html
def text_html(string):
    txt_html = """
    <style>
    .h5 {
        background-color: #FFFFFF;
        font-size: 25px;
    }
    </style> 
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    <h5><b>"""+string+"""</b></h5> 
    """
    return txt_html


def DrawLaundry_Points(latitude, longitude, map,string, list_box):
    if string in list_box:
        if(string == "bancos"):
            folium.Marker(location=[latitude,longitude ],popup=string,icon=folium.Icon(color='blue', icon="euro")).add_to( map )
        elif(string == "education"):
            folium.Marker(location=[latitude,longitude ],popup=string,icon=folium.Icon(color='blue', icon="book")).add_to( map )
        elif(string == "supermercados"):
            folium.Marker(location=[latitude,longitude ],popup=string,icon=folium.Icon(color='blue', icon="shopping-cart")).add_to( map )
        elif(string == "tiendas"):
            folium.Marker(location=[latitude,longitude ],popup=string,icon=folium.Icon(color='blue', icon="tag")).add_to( map )
        elif(string == "lavanderias"):
            folium.Marker(location=[latitude,longitude ],popup=string,icon=folium.Icon(color='red', icon="tint")).add_to( map )
        elif(string == "parques"):
            folium.Marker(location=[latitude,longitude ],popup=string,icon=folium.Icon(color='green', icon="tree-conifer")).add_to( map )
        elif(string == "gimnasios"):
            folium.Marker(location=[latitude,longitude ],popup=string,icon=folium.Icon(color='blue', icon="flash")).add_to( map )
        elif(string == "restaurante"):
            folium.Marker(location=[latitude,longitude ],popup=string,icon=folium.Icon(color='blue', icon="cutlery")).add_to( map )
        else:
            folium.Marker(location=[latitude,longitude ],popup=string,icon=folium.Icon(color='blue', icon="info-sign")).add_to( map )

    


def main():

#Configuración estilo
    # Hacemos que el gráfico sea a toda pagina
    st.set_page_config(layout="wide")
    data = []
    huff_model = pd.DataFrame(data, columns=[])
    list_of_points = pd.DataFrame(data, columns=[])
    seccensales_geojson = seccensales_data()
    laundry, huff_model, list_of_points = test_output_date()
    dataset_ine = dataset_ine_get()
    #laundry, huff_model, list_of_points = get_api_output_date('Calle de perez galdos 42, Valencia, Valencia')


# Título del CM
    Title_html = """
        <style>
            .title h1{
            user-select: none;
            font-size: 43px;
            color: black;
            background-color: #ffffff;
            text-align: center;
            }
            .div {
            background-color: #e2e2e2;
            text-align: center;
            }
        </style> 

        <div class="title">
            <h1>EDEM/Jeff - Location Intelligence</h1>
        </div>
        """
    st.markdown(Title_html, unsafe_allow_html=True)

# Cuadro de introducción texto + bot
    street_name_prev = ""
    street_name = st.text_input("Inserte aqui una dirección")
    if street_name:
        if street_name == street_name_prev:
            #laundry, huff_model, list_of_points  = get_api_output_date(street_name)
            street_name_prev = street_name
            print(street_name)
    if not huff_model.empty:
        lavan_card = card_db("Locales Competencia", str(int(laundry['lavanderias'][0])))
        atractividad_card= card_db("Atracción entorno", str(format(laundry['atractividad_percent'][0]*100, ".2f")+"%"))
        habitantes_card = card_db("Mercado total", str(int(laundry['habitantes_total'][0])))
        c1, c2, c3= st.columns((5, 5, 5))
        c1.markdown(lavan_card, unsafe_allow_html=True)
        c2.markdown(atractividad_card, unsafe_allow_html=True)
        c3.markdown(habitantes_card, unsafe_allow_html=True)

        options = st.multiselect(
            'Filtro puntos de interes:',
            list_of_points['type'].unique(),
            list_of_points['type'].unique())

        c1map, c2map= st.columns((8, 5))
        map = folium.Map(location=[laundry['latitude'], laundry['longitude']], zoom_start=16, tiles='stamentoner', width='100%', height='100%')
        folium.TileLayer('CartoDB positron').add_to(map)
        choropleth = folium.Choropleth(
            geo_data=seccensales_geojson,
            data=huff_model,
            name='Probabilidad Huff', 
            columns=["properties_coddistsec", "Huff_Prob"],
            key_on="feature.properties.coddistsec",
            fill_color='YlGnBu', 
            fill_opacity=0.70, 
            line_opacity=1,
            legend_name='Probabilidad huff',
            smooth_factor=0
        ).add_to(map)

        folium.Marker(
            location=[laundry['latitude'], laundry['longitude']],
            popup="Futura Lavanderia",
            icon=folium.Icon(color='purple', icon="info-sign")).add_to( map )
        folium.CircleMarker(
            location=[laundry['latitude'], laundry['longitude']],
            radius=10,
            popup="Futura Tienda",
            color="#f0c33c",
            fill=True,
            fill_color="#3186cc",
        ).add_to(map)

        polygon_isochrone = shapely.wkt.loads(laundry['isochrone_500m'][0])
        sim_geo = gpd.GeoSeries(polygon_isochrone).simplify(tolerance=0.001)
        geo_j = sim_geo.to_json()
        geo_j = folium.GeoJson(data=geo_j,
                        name='Isocrona',
                        style_function=lambda x: {'fillColor': 'orange'})
        folium.Popup(laundry['isochrone_500m']).add_to(geo_j)
        geo_j.add_to(map)

        folium.LayerControl().add_to(map)
        choropleth.geojson.add_child(
            folium.features.GeoJsonTooltip(['coddistsec'], labels=False)
        )

        list_of_points.apply(lambda row: DrawLaundry_Points(row['latitude'],row['longitude'],map,row['type'],options), axis=1)
        c1map.map = folium_static(map, 900, 700)
        
        chart_data = laundry[list_of_points['type'].unique()]
        chart_data_flip = chart_data.transpose().sort_values(0)

        getbestsec= huff_model.nlargest(5, 'Huff_Prob')
        getbestsec.reindex(getbestsec['properties_coddistsec'].unique())

        
        st.bar_chart(chart_data_flip)
        st.bar_chart(getbestsec)




if __name__ == '__main__':
    main()
