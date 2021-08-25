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
    # geo_json_data = json.loads(requests.get(geojson).text)

    # LEYENDO JSON PARA SUBDIVISIÓN
    input_dict_div = json.loads(requests.get(geojson).content)

    # TABLA CSV, SUBDIVISIONES
    datosDiv = "https://raw.githubusercontent.com/hectorflores329/mapa_insumos/main/municipios/csv/Censo2017_Poblacion1_ZONLOC.csv"
    dfDiv = pd.read_csv(datosDiv)

    dfSubc = dfDiv[dfDiv["COD_COMUNA"] == com]
    divi = dfSubc["COD_ZonLoc"].unique().tolist()
    divi

    # MAPA
    m = folium.Map(
        location=[-33.48621795345005, -70.66557950912359],
        zoom_start=13,
        
        )


    # AGREGACIÓN DE POLÍGONOS
    feature_group = FeatureGroup(name="MUNICIPIOS", show=False)

    # for i in divi:
    i = 1101011001     
    df_ = dfDiv

    df_ = df_[df_["COD_ZonLoc"] == i]
    indx_ = df_.index[0]

    output_dict_ = [x for x in input_dict_div['features'] if x['properties']['COD_ZonLoc'] == i]

    salida_ = {'type':'FeatureCollection','features':output_dict_}

    htmlDiv="""

        <style>
            *{
                font-family: Arial, Tahoma;
                font-size: 13px;
            }
            
            li{
                list-style:none;
                margin-left: -40px;
            }

            img{
                width: 70%;
                height: auto;
            }

            .banner{
                width: 100%;
                height: auto;
            }
        </style>
        <br>
        <h3><center>COLECCIÓN MUNICIPIOS</center></h3>
        <div>
            <ul>
                <li><b>REGIÓN:</b> """ + str(df_["REGION"][indx_]) + """</li>
                <li><b>PROVINCIA</b> """ + str(df_["PROVINCIA"][indx_]) + """</li>
                <li><b>COMUNA:</b> """ + str(df_["NOMBRE_COM"][indx_]) + """</li>
            </ul>
        </div>
    """

    iframeDiv = folium.IFrame(html=htmlDiv, width=250, height=300)
    _popupDiv = folium.Popup(iframeDiv, max_width=2650)



    geojsonDiv = folium.GeoJson(json.dumps(salida_),
                    tooltip = folium.GeoJsonTooltip(fields=["Nombre"],
                    aliases = ['NOMBRE: ']),
                    ).add_to(feature_group)

    popupDiv = _popupDiv
    popupDiv.add_to(geojsonDiv)

    feature_group.add_to(m)
    folium.LayerControl().add_to(m)

    return m._repr_html_()


if __name__ == '__main__':
    app.run()
