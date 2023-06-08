from beebotte import *
import time
import paho.mqtt.client as mqtt
from datetime import datetime
import plotly.express as px
import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from codeVelo import*
import folium
import googlemaps

def getMapInfo():
    
    #setBikeInfos()

    marker_data = getBikeInfos()

    m = folium.Map(location=[marker_data[0]["latitude"], marker_data[0]["longitude"]], zoom_start=11.8)


    # Add markers to the map
    for marker in marker_data:
        popup_content = "test"
        
        folium.Marker(
            location=[marker["latitude"], marker["longitude"]],
            icon=folium.Icon(color = 'blue', icon="bicycle", prefix = 'fa'),
            popup= str(marker['dispos']) + " available"
        ).add_to(m)


    return m

#############################

googleKey = 'AIzaSyAfCxMJaXGhI_548VG75KfrjrGqufU9Ha8'
gmaps = googlemaps.Client(key = googleKey)

col1, col2 = st.columns([4,1])

#setBikeInfos()  

with col1:
    
    my_map = st.empty()
    m = getMapInfo()
    my_map.empty()
    my_map.markdown(m._repr_html_(), unsafe_allow_html=True)

with col2:
    
    st.title("Fill in your information")

    st.markdown(
        """
        <style>
        .stTextInput {
            width: 100% !important;
        }
        .stButton {
            width: 100% !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    
    with st.form("Position Form", clear_on_submit=False):
        location_search = st.text_input("Enter a location", value = "Pizza Papa Comédie, Montpellier")
        submitted = st.form_submit_button("Submit")
        reset = st.form_submit_button("Reset")

        if submitted:
            
            with col1:
              
                #get the researched point coordinates
                geocode_result = gmaps.geocode(location_search)
                
                try:
                    uLatitude = geocode_result[0]["geometry"]["location"]["lat"]
                    uLongitude = geocode_result[0]["geometry"]["location"]["lng"]

                    m = folium.Map(location=[uLatitude, uLongitude], zoom_start=15)
                    
                    #add the researched point
                    folium.Marker(
                        location=[uLatitude, uLongitude],
                        popup=location_search,
                        icon=folium.Icon(icon="location-dot", color='red', prefix='fa')
                    ).add_to(m)

                    #add the closest bike
                    nearestBike = getClosestPosition(float(uLatitude), float(uLongitude), getBikeInfos())
                    folium.Marker(
                        location=[nearestBike['latitude'], nearestBike['longitude']],
                        popup= str(nearestBike['dispos']) + " available",                    
                        icon=folium.Icon(icon="bicycle", color = 'blue', prefix = 'fa')
                    ).add_to(m)
                    
                    start_lat, start_lng = float(uLatitude), float(uLongitude)
                    end_lat, end_lng = nearestBike['latitude'], nearestBike['longitude']

                    gmaps = googlemaps.Client(key=googleKey)
                    directions = gmaps.directions(
                        (start_lat, start_lng), 
                        (end_lat, end_lng),
                         mode = 'walking' 
                    )
                    
                    polyline = directions[0]["overview_polyline"]["points"]
                    decoded_polyline = googlemaps.convert.decode_polyline(polyline)

                    polyline_coordinates = [(coord['lat'], coord['lng']) for coord in decoded_polyline]
                
                    folium.PolyLine(
                        locations=polyline_coordinates,
                        color='red',
                        weight=2,
                        opacity=1
                    ).add_to(m)

                    my_map.empty()
                    my_map.markdown(m._repr_html_(), unsafe_allow_html=True)
                except:
                    print("error")
                    with col2:
                        st.write("Unable to find the location")
               

        if reset:
            my_map = st.empty()
            m = getMapInfo()
            my_map.empty()
            my_map.markdown(m._repr_html_(), unsafe_allow_html=True)


from meteo import*

data = getMeteo()

# Content for row 3

if 'rain' in data['weather'][0]['description']:
    st.header("Maybe not the best time to ride a bike")
else:
    st.header("Let's go !")

icon = data['weather'][0]['icon']
image_url = "https://openweathermap.org/img/wn/"+icon+"@2x.png"
print("IMAGE  : ", image_url)
st.image(image_url, use_column_width=False)
st.write("Temperature : ", str(round(data['main']['temp']-273.15)) + " °C")
st.write("Feels like : ", str(round(data['main']['feels_like']-273.15)) + " °C")