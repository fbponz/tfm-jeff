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
    st.title('TFM Jeff')
    
    c1, c2= st.columns((1, 1))

    # Mapa
    map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

    st.map(map_data)

    st.text_input("Introduzca la direccion:"
                    " Ejemplo: Calle ", key="name")

    # You can access the value at any point with:
    st.session_state.name

    # Gráfico de
    chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

    c2.bar_chart(chart_data)

      # Gráfico de
    chart_data2 = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

    c1.bar_chart(chart_data2)

        # Add a selectbox to the sidebar:
    add_selectbox = st.sidebar.selectbox(
        'How would you like to be contacted?',
        ('Email', 'Home phone', 'Mobile phone')
    )

    # Add a slider to the sidebar:
    add_slider = st.sidebar.slider(
        'Select a range of values',
        0.0, 100.0, (25.0, 75.0)
    )

if __name__ == '__main__':
    main()
