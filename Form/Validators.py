import re
import streamlit as st
from Expa.Register import Register

class Validators():
    def __init__(self) -> None:
        self.user = {}
        self.__errors = []
        self.__email_error = ""
        self.__password_errors = []

    def validate_password(self,password):
        """ 
         Validar los passwords utilizando los constraints de EXPA
        """
        if password == "": 
            return None
        if len(password) < 8:
            self.__password_errors.append("El password es de minimo 8 caracteres")
            yield "El password es de minimo 8 caracteres"
        if password == password.lower():
            self.__password_errors.append("El password debe tener almenos una mayuscula")
            yield "El password debe tener almenos una mayuscula"
        if password == password.upper():
            self.__password_errors.append("El password debe tener almenos una minúscula")
            yield "El password debe tener almenos una minúscula"

    def validate_email(self,email):
        """ Validacion de email:
            # Usando expresiones regulares
        """
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if email == "": 
            return None
        if not (re.fullmatch(regex, email)):
            self.__email_error = "Email no valido"
            return "Email no valido"
            
    def __validate__(self,user):
        """ Validar espacios vacios """
        for key,value in user.items():
            if not value:
                self.__errors.append(f"Por favor llenar los campos solicitados: {key}") 

    def last_check(self,user):
        """ # Checar que no hayan campos vacios 
            # Checar que el registro a expa este check
            # Registro en Expa y Podio
        """
        self.user = user
        #validar si algun campo esta vacio
        self.__validate__(self.user)

        #Si hay algun error o errores, lanzara una alerta
        if self.__email_error:
            self.__errors.append(self.__email_error)
        if self.__password_errors:
            self.__errors.extend(self.__password_errors)
        if self.__errors:      
            for err in self.__errors:
                st.warning(err)
        else:
            register = Register(self.user)
            register.verify_university()
            register.podio_register()
            return "Registro Exitoso"
            """ #Registro en Expa
            response = register.register()
            response_dict = dict(response.json())
            print(f'Response Status: {response.status_code} Response Text: {response.text}') 
        
            if 'errors' in response_dict or response.status_code != 200:
                for error, message in response_dict['errors'].items():
                    st.warning(f'{error.capitalize()} {message[0]}')
            else:
                #Registro en Podio
                register.podio_register()
                return "Registro Exitoso" """
            