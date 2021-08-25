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

    for i in divi:
        
        _union = i
        # print(cut)
        
        df_ = dfDiv

        df_ = df_[df_["Id_Union"] == _union]
        indx_ = df_.index[0]

        output_dict_ = [x for x in input_dict_div['features'] if x['properties']['Id_Union'] == _union]

        salida_ = {'type':'FeatureCollection','features':output_dict_}

        if(df_["COD_GLA"][indx_] is np.nan):
            codGla = "No definido"
        else:
            codGla = df_["COD_GLA"][indx_]

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
            <center><img class="banner" src="https://raw.githubusercontent.com/Sud-Austral/mapa_glaciares/main/img/Glaciares.jpg" alt="Data Intelligence"/></center>
            <br>
            <h3><center>""" + str(df_["Nombre_GLA"][indx_]) + """</center></h3>
            <div>
                <ul>
                    <li><b>REGIÓN:</b> """ + str(df_["NOM_REGION"][indx_]) + """</li>
                    <li><b>PROVINCIA</b> """ + str(df_["NOM_PROVIN"][indx_]) + """</li>
                    <li><b>COMUNA:</b> """ + str(df_["NOM_COMUNA"][indx_]) + """</li>
                    <br>
                    <li><b>CÓDIGO GLACIAR:</b> """ + str(codGla) + """</li>
                    <li><b>NOMBRE DE GLACIAR:</b> """ + str(df_["NOMBRE"][indx_]) + """</li>
                    <li><b>SUBSUBCUENCA:</b> """ + str(df_["NOM_SSUBC"][indx_]) + """</li>
                    <br>
                    <li><b>Q1 (Ene-Abr) Mínima (ha):</b> """ + str('{:,}'.format(round(df_["q1_Min"][indx_]), 1).replace(',','.')) + """</li>
                    <li><b>Q1 (Ene-Abr) Máxima (ha):</b> """ + str('{:,}'.format(round(df_["q1_Max"][indx_]), 1).replace(',','.')) + """</li>
                    <br>
                    <li><b>Q2 (May-Dic) Mínima (ha):</b> """ + str('{:,}'.format(round(df_["q2_Min"][indx_]), 1).replace(',','.')) + """</li>
                    <li><b>Q2 (May-Dic) Máxima (ha):</b> """ + str('{:,}'.format(round(df_["q2_Max"][indx_]), 1).replace(',','.')) + """</li>
                </ul>
                <center><img src="https://raw.githubusercontent.com/Sud-Austral/mapa_glaciares/main/img/logo_DataIntelligence_normal.png" alt="Data Intelligence"/></center>
            </div>
        """

        iframeDiv = folium.IFrame(html=htmlDiv, width=290, height=400)
        _popupDiv = folium.Popup(iframeDiv, max_width=2650)

        def colormap(feature):
            if feature["properties"]["idZonGlac"] > 0:
                r = lambda: random.randint(0,255)
                hexaColor = '#%02X%02X%02X' % (r(),r(),r())
            else:
                hexaColor = 'transparent'

            return hexaColor

        geojsonDiv = folium.GeoJson(json.dumps(salida_),
                       tooltip = folium.GeoJsonTooltip(fields=["NOM_SSUBC"],
                       aliases = ['SUBSUBCUENCA: ']),
                       style_function=lambda feature: {
                            "fillColor": colormap(feature)
                        },
                        ).add_to(feature_group)

        popupDiv = _popupDiv
        popupDiv.add_to(geojsonDiv)

    feature_group.add_to(m)
    folium.LayerControl().add_to(m)

    return m._repr_html_()


if __name__ == '__main__':
    app.run()
