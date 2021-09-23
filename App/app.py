
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
import streamlit as st
import folium
from streamlit_folium import folium_static

@st.cache(allow_output_mutation=True)
def seccensales_data():
    with open('data/seccensales.JSON') as f: 
        seccensales_geojson = json.load(f)
    for idx in range(len(seccensales_geojson['features'])):
        seccensales_geojson['features'][idx]['properties']['coddistsec'] = int(seccensales_geojson['features'][idx]['properties']['coddistsec'])
    return seccensales_geojson

@st.cache
def test_output_date():
    with open('data_test/sample.json') as f: 
        api_request = json.load(f)
    df = pd.json_normalize(api_request['49'])
    data3 = json.loads(df['Prob_Huff'][0])
    df2 = pd.DataFrame.from_dict(data3, orient="index")
    return df, df2

def get_api_output_date(street_name):
    r =requests.post('https://europe-west6-tfmedem.cloudfunctions.net/API_TFM', json={'street_name':street_name})
    json_object = json.dumps(r.json(), indent = 4)
    data = json.loads(json_object)
    df = pd.json_normalize(data['49'])
    data3 = json.loads(df['Prob_Huff'][0])
    df2 = pd.DataFrame.from_dict(data3, orient="index")
    return df, df2

def card_db(string, value):
    st.title(string)
    st.text(value)

def main():

#Configuración estilo
    # Hacemos que el gráfico sea a toda pagina
    st.set_page_config(layout="wide")
    data = []
    huff_model = pd.DataFrame(data, columns=[])
    seccensales_geojson = seccensales_data()
    #laundry, huff_mode = test_output_date()
    #laundry, huff_mode = get_api_output_date('Calle de perez galdos 42, Valencia, Valencia')


# Título del CM
    st.title('Location Intelligence, TFM-Jeff/EDEM')

# Cuadro de introducción texto + bot
    c1, c2= st.columns((8, 5))
    street_name = c1.text_input("Por favor, introduzca una dirección")
    if street_name:
        laundry, huff_model = get_api_output_date(street_name)
        print(street_name)


    if not huff_model.empty:
        # Mapa
            # center on Liberty Bell
        map = folium.Map(location=[39.46994829189022, -0.37787440832473984], width='100%', height='100%')
            # add marker for Liberty Bell
        tooltip = "MR. Jeff"

        folium.Choropleth(
            geo_data=seccensales_geojson,
            data=huff_model,
            name='choropleth', 
            columns=["properties_coddistsec", "Huff_Prob"],
            key_on="feature.properties.coddistsec",
            fill_color='YlGnBu', 
            fill_opacity=0.70, 
            line_opacity=1,
            legend_name='Distancia Lavanderia',
            smooth_factor=0
        ).add_to(map)
        
        folium_static(map)


    # Gráfico de barras 1
        chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a', 'b', 'c'])

        st.bar_chart(chart_data)

    # Gráfico debarras 2
        chart_data2 = pd.DataFrame(
        np.random.randn(3, 1),
        columns=['a'])

        st.bar_chart(chart_data2)

if __name__ == '__main__':
    main()
