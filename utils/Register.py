import requests 
import json
from utils.data import SEGMENTACION
from utils.Podio import Podio

class Register():
    def __init__(self,user) -> None:
        self.user = user
        self.__lc_expa_id = 2008 #default es Virtual Expansion

    def segmentacion(self):
        """Metodo para verificar la universidad correspondiente"""
        universidad = self.user['Universidad']
        for key in SEGMENTACION.keys():
            if universidad in SEGMENTACION[key][0]:
                self.__lc_expa_id = SEGMENTACION[key][1]
                self.__lc_podio_id = SEGMENTACION[key][2]
                break
     
    def expa_register(self):
        """ Registro en EXPA """
        self.__expa_user = {
            "user": {
                "first_name": self.user['First Name'],
                "last_name": self.user['Last Name'],
                "email": self.user['Email'],
                "country_code": "+507",
                "phone": self.user['Phone'],
                "password": self.user['Password'],
                "lc": self.__lc_expa_id, 
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

    def podio_register(self):
        """ Verificar la segmentación y hacer el registro en Podio """
        self.segmentacion()
        podio = Podio()
        podio.register_SU(self.user,self.__lc_podio_id)