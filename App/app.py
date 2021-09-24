
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
import altair as alt

@st.cache(allow_output_mutation=True)
def seccensales_data(dataset_ine):
    with open('data/seccensales.JSON') as f: 
        seccensales_geojson = json.load(f)
    for idx in range(len(seccensales_geojson['features'])):
        seccensales_geojson['features'][idx]['properties']['coddistsec'] = int(seccensales_geojson['features'][idx]['properties']['coddistsec'])
        seccensales_geojson['features'][idx]['properties']['Seccion Censal'] = seccensales_geojson['features'][idx]['properties']['coddistsec']

        renta_med, habitantes = rentamed_poblacion(seccensales_geojson['features'][idx]['properties']['coddistsec'],dataset_ine)
        seccensales_geojson['features'][idx]['properties']['Renta Media'] = renta_med
        seccensales_geojson['features'][idx]['properties']['Habitantes'] = habitantes
    return seccensales_geojson

def rentamed_poblacion(seccioncensal,dataset_ine):
    dataset_ine_row = dataset_ine.loc[dataset_ine['Code'] == seccioncensal]
    if dataset_ine_row.empty:
        renta_med_conver = 'NaN'
        habitantes_conver = 'NaN'
    else:
        renta_med = dataset_ine_row.renta_media_hogar.values
        habitantes = dataset_ine_row.habitantes.values
        renta_med_conver = int(float(renta_med)*1000)
        habitantes_conver = int(float(habitantes))
    return renta_med_conver, habitantes_conver


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


def get_api_output_date(street_name):
    r =requests.post('https://europe-west6-tfmedemv2.cloudfunctions.net/API_TFM', json={'street_name':street_name})
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
        color: #32B0E1;
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

def draw_map(laundry, seccensales_geojson, huff_model,list_of_points, options):
    
    map = folium.Map(location=[laundry['latitude'], laundry['longitude']], zoom_start=16, tiles='stamentoner')
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
        folium.features.GeoJsonTooltip(['Seccion Censal', 'Renta Media', 'Habitantes'], labels=True)
    )
    list_of_points.apply(lambda row: DrawLaundry_Points(row['latitude'],row['longitude'],map,row['type'],options,laundry), axis=1)
    return map


def DrawLaundry_Points(latitude, longitude, map,string, list_box,laundry):
    if string in list_box:
        if(string == "bancos"):
            string_popup = "En 500m hay "+str(int(laundry.bancos.values))+" Bancos."
            folium.Marker(location=[latitude,longitude ],popup=string_popup,icon=folium.Icon(color='blue', icon="euro")).add_to( map )
        elif(string == "education"):
            string_popup = "En 500m hay "+str(int(laundry.education.values))+" Centros Educativos."
            folium.Marker(location=[latitude,longitude ],popup=string_popup,icon=folium.Icon(color='blue', icon="book")).add_to( map )
        elif(string == "tiendas"):
            string_popup = "En 500m hay "+str(int(laundry.tiendas.values))+" Tiendas."
            folium.Marker(location=[latitude,longitude ],popup=string_popup,icon=folium.Icon(color='blue', icon="tag")).add_to( map )
        elif(string == "lavanderias"):
            string_popup = "En 500m hay "+str(int(laundry.lavanderias.values))+" lavanderias."
            folium.Marker(location=[latitude,longitude ],popup=string_popup,icon=folium.Icon(color='red', icon="tint")).add_to( map )
        elif(string == "parques"):
            string_popup = "En 500m hay "+str(int(laundry.parques.values))+" parques."
            folium.Marker(location=[latitude,longitude ],popup=string_popup,icon=folium.Icon(color='green', icon="tree-conifer")).add_to( map )
        elif(string == "gimnasios"):
            string_popup = "En 500m hay "+str(int(laundry.gimnasios.values))+" gimnasios."
            folium.Marker(location=[latitude,longitude ],popup=string_popup,icon=folium.Icon(color='blue', icon="flash")).add_to( map )
        elif(string == "restaurante"):
            string_popup = "En 500m hay "+str(int(laundry.restaurante.values))+" restaurantes."
            folium.Marker(location=[latitude,longitude ],popup=string_popup,icon=folium.Icon(color='blue', icon="cutlery")).add_to( map )
        else:
            string_popup = "Información no disponible"
            folium.Marker(location=[latitude,longitude ],popup=string_popup,icon=folium.Icon(color='blue', icon="info-sign")).add_to( map )

def renta_media_huff_proba(huff_model, dataset_ine):
    selected_row =huff_model.nlargest(5, ['Huff_Prob'])
    prob_huff_med = (selected_row['Huff_Prob'].sum()/5)
    secciones_censales_huff = selected_row['properties_coddistsec'].unique()
    renta_media = 0
    for i in secciones_censales_huff:
        for _, r in dataset_ine.iterrows():
            if r["Code"] == i:
                renta_media = renta_media+ r["Renta neta media por persona "]
    renta_media = (renta_media/5)*1000
    return renta_media, prob_huff_med 


def main():

#Configuración estilo
    # Hacemos que el gráfico sea a toda pagina
    st.set_page_config(layout="wide")
    data = []
    huff_model = pd.DataFrame(data, columns=[])
    list_of_points = pd.DataFrame(data, columns=[])
    dataset_ine = dataset_ine_get()
    seccensales_geojson = seccensales_data(dataset_ine)

    #laundry, huff_model, list_of_points = test_output_date()



# Título del CM
    logo1,logo2, logo3= st.columns((5, 5, 5))
    logo2.image("img/logo.png")

# Cuadro de introducción texto + bot
    dir1, dir2= st.columns((5, 5))
    street_name_prev = ""
    street_name = dir1.text_input("Inserte aqui una dirección")
    if street_name:
        if street_name != street_name_prev:
            print(street_name)
            laundry, huff_model, list_of_points  = get_api_output_date(street_name)
            street_name_prev = street_name

    if not huff_model.empty:
        #enriquezer el GEOJSON
        renta_med, prob_huff_med= renta_media_huff_proba(huff_model, dataset_ine)        

        poi_card = card_db("Puntos de interes totales", str(int(laundry['total_poi'][0])))
        lavan_card = card_db("Lavanderias Competencia", str(int(laundry['lavanderias'][0])))
        rentamedia_card = card_db("Renta neta persona", str(int(renta_med))+" €")
        huff_card= card_db("Probabilidad Huff", str(format(prob_huff_med*100, ".2f")+"%"))
        marketpot_card = card_db("Mercado Potencial", str(int(laundry['habitantes_total'][0])))
        marketmeta_card = card_db("Mercado meta", str(int(laundry['habitantes_total'][0]*prob_huff_med)))
        c1, c2, c3, c4, c5, c6= st.columns((5, 5, 5, 5, 5, 5))
        c1.markdown(poi_card, unsafe_allow_html=True)
        c2.markdown(lavan_card, unsafe_allow_html=True)
        c3.markdown(rentamedia_card, unsafe_allow_html=True)
        c4.markdown(marketpot_card, unsafe_allow_html=True)
        c5.markdown(huff_card, unsafe_allow_html=True)
        c6.markdown(marketmeta_card, unsafe_allow_html=True)

        options = dir2.multiselect(
            '',
            list_of_points['type'].unique(),
            list_of_points['type'].unique())

        st.markdown('###')

        map =draw_map(laundry, seccensales_geojson, huff_model, list_of_points, options)

        folium_static(map,2324,800)    

if __name__ == '__main__':
    main()
