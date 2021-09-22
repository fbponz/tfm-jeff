# Importamos las librerias
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify, render_template, url_for
import pickle
import time
import streamlit as st



def main():

    st.set_page_config(layout="wide")

    # Título del CM
    st.title('Location Intelligence')
    
    c1, c2= st.columns((3, 4))

    # Mapa
    map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

    c2.map(map_data)

    c1.text_input("Introduzca la direccion:"
                    " Ejemplo: Calle ", key="name")

    # You can access the value at any point with:
    st.session_state.name

    # Gráfico de
    chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

    c1.bar_chart(chart_data)

      # Gráfico de
    chart_data2 = pd.DataFrame(
     np.random.randn(3, 1),
     columns=['a'])

    c1.bar_chart(chart_data2)

        # Add a selectbox to the sidebar:
    add_selectbox = st.sidebar.selectbox(
        'Puntos de interés',
        ('Lavanderias', 'Hospital', 'Tiendas GGSS')
    )

    # Add a slider to the sidebar:
    add_slider = st.sidebar.slider(
        'Radio Km',
        0.0, 100.0, (25.0, 75.0)
    )

if __name__ == '__main__':
    main()
