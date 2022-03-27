from pypodio2 import api

import streamlit as st
from utils.data import NIVEL_INGLES,PODIO_REFERENTES
import json

""" 
TIPOS = 'text', 'category', 'embed', 'date'
PARA CADA TIPO:
    TEXT: item.get('fields')[i]['values'][0]['value']
    CATEGORY: item.get('fields')[i]['values'][0]['value']['text']
    EMBED: item.get('fields')[i]['values'][0]['url']['url']
    DATE: item.get('fields')[i]['values][0]['start_date_utc']
""" 

#PODIO API
client_id = st.secrets["PODIO_CLIENT_ID"]
client_secret = st.secrets["PODIO_CLIENT_SECRET"]
username = st.secrets["PODIO_USERNAME"]
password = st.secrets["PODIO_PASSWORD"]
ogt_workspace_id = int(st.secrets["PODIO_OGT_WORKSPACE_ID"])
ogt_app_id = int(st.secrets["PODIO_OGT_APP_ID"])

class Podio:
    def __init__(self) -> None:
        self.podio = api.OAuthClient(
            client_id,
            client_secret,
            username,
            password,    
        )

    def register_SU(self,user,lc_id):
        referral_id = PODIO_REFERENTES[user['Referral']]
        nivel_ingles = NIVEL_INGLES[user['Ingles']]

        attributes = {
            "fields": [{
                    "field_id": 233431600,
                    "label": "Nombre y Apellido",
                    "values": [f'{user["First Name"]} {user["Last Name"]}']
                },
                {
                    "type": "category",
                    "field_id": 233431604,
                    "label": "Home Entity",
                    "values": [lc_id],
                },
                {
                    "type": "phone",
                    "field_id": 233431602,
                    "label": "Teléfono",
                    "values": [{"type": "mobile", "value": user['Phone']}]
                },
                {
                    "type": "email",
                    "field_id": 233431603,
                    "label": "Email",
                    "values": [{"type": "other","value": user['Email']}]
                },
                {
                    "type": "text",
                    "field_id": 233431609,
                    "label": "Carrera",
                    "values": [user['Background']]
                },
                {
                    "type": "text",
                    "field_id": 233431610,
                    "label": "Universidad",
                    "values": [user['Universidad']]
                },
                {
                    "type": "category",
                    "field_id": 233431628,
                    "label": "Status",
                    "values":[9] #SU
                },
                {
                    "type": "category",
                    "field_id": 233431617,
                    "label": "Como me enteré del programa?",
                    "values":[referral_id] #Numero de podio
                },
                {
                    "type": "category",
                    "field_id": 237376300,
                    "label": "Nivel de Ingles",
                    "values": [nivel_ingles],
                },{
                    "type": "text",
                    "field_id": 235124236,
                    "label": "Edad",
                    "values":user['Edad']              
                },
                {
                    "type": "category",
                    "field_id": 233431608,
                    "label": "Estudios",
                    "values": [user["Estudios"]]
                }]
            }
        """ Utilizando los atributos ya propuestos, creamos el EP """
        item_response = self.podio.Item.create(ogt_app_id,attributes)
        #ref_type,ref_id = item_response["presence"]["ref_type"],item_response["presence"]["ref_id"]
    
    def iterate_Podio(self,cantidad):
        self.EPs = []
        self.items = self.podio.Application.get_items(app_id=ogt_app_id,limit = cantidad).get('items')

        for item in self.items:
            EP = dict()   
            fields = item.get("fields")
            for field in fields:
                tipo = field["type"]
                label = field["label"]
                if tipo == "phone":
                    valor = field['values'][0]['value']
                    EP[label] = valor
                if tipo == "text":
                    valor = field['values'][0]['value']
                    EP[label] = valor
                if tipo == "category":
                    valor = field['values'][0]['value']['text']
                    EP[label] = valor
                if tipo == "embed":
                    valor = field['values'][0]['embed']['url']
                    EP[label] = valor
                if tipo == "date":
                    valor = field['values'][0]['start_date_utc']
                    EP[label] = valor
            self.EPs.append(EP)

    def create_SU_json(self):
        with open("EPs.json",'w',encoding='utf-8') as f:
            try:
                f.write(json.dump(self.EPs,f,ensure_ascii=False)) 
            except TypeError:
                print("cheverito") 
                
    def create_items_json(self):
        with open("EP.json",'w',encoding='utf-8') as f:
            f.write(json.dump(self.items,f,ensure_ascii=False)) 




""" 
#Run in CLI

from pypodio2 import api
import streamlit as st
import json
client_id = st.secrets["PODIO_CLIENT_ID"]
client_secret = st.secrets["PODIO_CLIENT_SECRET"]
username = st.secrets["PODIO_USERNAME"]
password = st.secrets["PODIO_PASSWORD"]
ogt_workspace_id = int(st.secrets["PODIO_OGT_WORKSPACE_ID"])
ogt_app_id = int(st.secrets["PODIO_OGT_APP_ID"])

podio = api.OAuthClient(
            client_id,
            client_secret,
            username,
            password,    
        )
cantidad = 1
items = podio.Application.get_items(app_id=ogt_app_id,limit = cantidad).get('items')

with open("EP.json",'w',encoding='utf-8') as f:
    f.write(json.dump(items,f,ensure_ascii=False)) 
"""




    