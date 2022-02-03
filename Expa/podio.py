from pypodio2 import api
import streamlit as st

#PODIO API
client_id = st.secrets["PODIO_CLIENT_ID"]
client_secret = st.secrets["PODIO_CLIENT_SECRET"]
username = st.secrets["PODIO_USERNAME"]
password = st.secrets["PODIO_PASSWORD"]
ogt_workspace_id = int(st.secrets["PODIO_OGT_WORKSPACE_ID"])
ogt_app_id = int(st.secrets["PODIO_OGT_APP_ID"])

class Podio:
    def __init__(self,user,podio_id,referral_id) -> None:
        self.podio = api.OAuthClient(
            client_id,
            client_secret,
            username,
            password,    
        )
        self.user = user
        self.__uni_podio_id = podio_id
        self.__referral = referral_id

    def create(self):
        self.attributes = {
            "fields": [{
                    "field_id": 233431600,
                    "label": "Nombre y Apellido",
                    "values": [f'{self.user["First Name"]} {self.user["Last Name"]}']
                },
                {
                    "type": "category",
                    "field_id": 233431604,
                    "label": "Home Entity",
                    "values": [self.__uni_podio_id],
                },
                {
                    "type": "phone",
                    "field_id": 233431602,
                    "label": "Teléfono",
                    "values": [{"type": "mobile", "value": self.user['Phone']}]
                },
                {
                    "type": "email",
                    "field_id": 233431603,
                    "label": "Email",
                    "values": [{"type": "other","value": self.user['Email']}]
                },
                {
                    "type": "text",
                    "field_id": 233431609,
                    "label": "Carrera",
                    "values": [self.user['Background']]
                },
                {
                    "type": "text",
                    "field_id": 233431610,
                    "label": "Universidad",
                    "values": [self.user['Universidad']]
                },
                {
                    "type": "category",
                    "field_id": 233431628,
                    "label": "Status",
                    "values":[9] #SU
                },{
                "type": "category",
                "field_id": 233431617,
                "label": "Como me enteré del programa?",
                "values":[self.__referral]
                }
                ]
            }
        """ Utilizando los atributos ya propuestos, creamos el EP """
        self.podio.Item.create(ogt_app_id,self.attributes)
    




    