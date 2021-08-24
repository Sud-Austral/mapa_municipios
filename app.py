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
   
    url = (
        "https://raw.githubusercontent.com/Sud-Austral/mapa_glaciares/main/json"
    )

    geojson = f"{url}/R10_AREA_Glac_ZONA_glac.json"

    m = folium.Map(
        location=[-33.48621795345005, -70.66557950912359],
        zoom_start=13,
        
        )


    geojson = folium.GeoJson(geojson, 
                    name="Municipios",
                    ).add_to(m)

    return m._repr_html_()


if __name__ == '__main__':
    app.run()
