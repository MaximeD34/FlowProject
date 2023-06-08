import requests
import streamlit as st

base_url = "https://api.openweathermap.org/data/2.5/weather"
api_key = "f6631d47496e48f8708633e39b716799"
HOURLY_API_KEY = "2bc31c9a1808fe3debbdad944461a627"

city= "Montpellier"


url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'

def getMeteo():
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json() 
    else:
        print('Error:', response.status_code)

    return data

# temperature = data['main']['temp']
# humidity = data['main']['humidity']
# wind_speed = data['wind']['speed']

# print(f'Temperature: {round((temperature - 273.15),2)}°C')
# print(f'Humidity: {humidity}%')
# print(f'Wind Speed: {wind_speed} m/s')