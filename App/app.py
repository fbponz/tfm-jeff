
# Importamos las librerias
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify, render_template, url_for
import pickle
import json
import random
import string
import time
import streamlit as st
import folium
from streamlit_folium import folium_static


huff_mode = pd.read_csv(r'C:\Users\user\Dropbox\Mi PC (DESKTOP-LD4N8IJ)\Desktop\GitHub\tfm-jeff\App\huff_mode_output.csv', sep=',', decimal='.')
laundry_seccensal = pd.read_csv(r'C:\Users\user\Dropbox\Mi PC (DESKTOP-LD4N8IJ)\Desktop\GitHub\tfm-jeff\App\laundry_seccensal_output.csv', sep=',', decimal='.')
with open('seccensales.JSON') as f: 
    seccensales_geojson = json.load(f)
for idx in range(len(seccensales_geojson['features'])):
    seccensales_geojson['features'][idx]['properties']['coddistsec'] = int(seccensales_geojson['features'][idx]['properties']['coddistsec'])

def main():

#Configuración estilo
    # Hacemos que el gráfico sea a toda pagina
    st.set_page_config(layout="wide")

    # Colunas del Dashboard
    c1, c2= st.columns((3, 4))

# Título del CM
    st.title('Location Intelligence')

# Cuadro de introducción texto + bot
    st.text_input("Por favor, introduzca una dirección",
    key=random.choice(string.ascii_uppercase)+str(random.randint(0,999999)))
    st.button("Iniciar Cálculos")
        
# Mapa
        # center on Liberty Bell
    map = folium.Map(location=[39.46994829189022, -0.37787440832473984], width='100%', height='100%')
        # add marker for Liberty Bell
    tooltip = "MR. Jeff"

    folium.Choropleth(
        geo_data=seccensales_geojson,
        data=huff_mode,
        name='choropleth', 
        columns=["properties.coddistsec", "Huff_Prob"],
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
