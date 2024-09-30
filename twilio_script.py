import os
from twilio.rest import Client
from twilio_config import *
import time

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json


import pandas as pd
import requests
from bs4  import BeautifulSoup
from tqdm import tqdm

from datetime import datetime

## ARMADO DEL URL

query = "Buenos Aires"

api_key = API_KEY_WAPI

url_clima = "http://api.weatherapi.com/v1/forecast.json?key=" + api_key + "&q=" + query + "&days=1&aqi=no&alerts=no"


response = requests.get(url_clima).json()

def get_forecast (response,i):

    fecha = response['forecast']['forecastday'][0]['hour'][i]["time"].split()[0]
    hora = int(response['forecast']['forecastday'][0]['hour'][i]["time"].split()[1].split(':')[0])
    condicion = response['forecast']['forecastday'][0]['hour'][i]["condition"]["text"]
    tempe = response['forecast']['forecastday'][0]['hour'][i]["temp_c"]
    rain = response['forecast']['forecastday'][0]['hour'][i]["will_it_rain"]
    prob_rain = response['forecast']['forecastday'][0]['hour'][i]["chance_of_rain"]

    return fecha, hora, condicion, tempe, rain, prob_rain

datos = []

for i in tqdm (range(24),colour="green"):
    datos.append(get_forecast(response,i))

    print(get_forecast(response,i))



columnas = ['Fecha', 'Hora', 'Condicion', 'Temperatura', 'Lluvia', 'Prob_de_lluvia']
df = pd.DataFrame(datos,columns=columnas)

df_rain = df[(df['Hora']>6) & (df['Hora']< 22)]
df_rain = df_rain[['Hora','Condicion']]
df_rain.set_index('Hora', inplace = True)


time.sleep(2)
account_sid = TWILIO_ACCOUNT_SID
auth_token = TWILIO_AUTH_TOKEN

client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body='\nHola! \n\n\n El pronostico de hoy '+ df['Fecha'][0] +' en ' + query +' es : \n\n\n ' + str(df_rain),
                     from_=PHONE_NUMBER,
                     to='+xx xx xxxx xxxx'
                 )

print('Mensaje Enviado ' + message.sid)



