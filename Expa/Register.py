import requests 
import json
from data.data import SEGMENTACION,PODIO_REFERRAL
from Expa.podio import Podio

class Register():
    def __init__(self,user) -> None:
        self.user = user
        self.__uni_expa_id = 193 #default
        self.__podio_ref_id = PODIO_REFERRAL[user['Referral']]
        
    def register(self):
        """ Registro en EXPA """
        self.__expa_user = {
            "user": {
                "first_name": self.user['First Name'],
                "last_name": self.user['Last Name'],
                "email": self.user['Email'],
                "country_code": "+507",
                "phone": self.user['Phone'],
                "password": self.user['Password'],
                "lc": self.__uni_expa_id, 
                "referral_type": self.user['Referral'],
                "allow_phone_communication": "true",
                "allow_email_communication": "true",
                "selected_programmes": [7,8,9]
            }
        } 
        reqUrl = "https://auth.aiesec.org/users.json"
        headersList = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
        "Content-Type": "application/json",
        }
        response = requests.request("POST", reqUrl, data=json.dumps(self.__expa_user), headers=headersList)
        return response

    def verify_university(self):
        """Metodo para verificar la universidad correspondiente"""
        universidad = self.user['Universidad']
        for key,value in SEGMENTACION.items():
            if universidad in SEGMENTACION[key][0]:
                self.__uni_expa_id = SEGMENTACION[key][1]
                self.__uni_podio_id = SEGMENTACION[key][2]
                break

    def podio_register(self):
        """ Hacer el registro en Podio """
        podio = Podio(self.user,self.__uni_podio_id,self.__podio_ref_id)
        podio.create()