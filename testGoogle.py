import streamlit as st
from codeVelo import *
import folium

def getMapInfo():
    #googleKey = 'AIzaSyAfCxMJaXGhI_548VG75KfrjrGqufU9Ha8'

    marker_data = getBikeInfos()

    m = folium.Map(location=[marker_data[0]["latitude"], marker_data[0]["longitude"]], zoom_start=3)

    # Add markers to the map
    for marker in marker_data:
        folium.Marker(
            location=[marker["latitude"], marker["longitude"]],
            icon=folium.Icon(color = 'red', icon="bicycle", prefix = 'fa')
        ).add_to(m)
    
    
    return m
    

