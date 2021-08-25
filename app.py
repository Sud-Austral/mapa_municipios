from flask import Flask
from flask import request
import pandas as pd
import numpy as np
import folium
import json
import random
import requests
from folium.plugins import HeatMapWithTime
from branca.element import Template, MacroElement
from folium import FeatureGroup, LayerControl, Map, Marker

app = Flask(__name__)

@app.route('/')
def mapa():
   
    # PARÁMETROS 
    com = request.args.get("comuna")
    com = str(com)

    # GEOJSON
    url = (
        "https://raw.githubusercontent.com/hectorflores329/mapa_insumos/main/municipios/json"
    )

    geojson = f"{url}/" + com + ".json"
    geo_json_data = json.loads(requests.get(geojson).text)

    # TABLA CSV, SUBDIVISIONES
    datosDiv = "https://raw.githubusercontent.com/Sud-Austral/mapa_glaciares/main/csv/R10_Lim_Glaciares_FINAL_ClipRegion.csv"
    dfDiv = pd.read_csv(datosDiv)

    dfSubc = dfDiv[dfDiv["COD_COMUNA"] == int(com)]
    divi = dfSubc["COD_ZonLoc"].unique().tolist()
    divi

    # MAPA
    m = folium.Map(
        location=[-33.48621795345005, -70.66557950912359],
        zoom_start=13,
        
        )


    geojson = folium.GeoJson(geo_json_data, 
                    name="Municipios",
                    ).add_to(m)

    return m._repr_html_()


if __name__ == '__main__':
    app.run()
