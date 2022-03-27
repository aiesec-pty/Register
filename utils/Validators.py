import re
import streamlit as st

class Validators():
    def __init__(self) -> None:
        self.__error = False

    def validate_password(self,password):
        """ 
         Validar los passwords utilizando los constraints de EXPA
        """
        if password == "": 
            return None
        if len(password) < 8:
            self.__error = True
            st.warning("El password es de minimo 8 caracteres")
        if password == password.lower():
            self.__error = True
            st.warning("El password debe tener almenos una mayuscula")
        if password == password.upper():
            self.__error = True
            st.warning("El password debe tener almenos una minúscula")

    def validate_email(self,email):
        """ Validacion de email:
            # Usando expresiones regulares
        """
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if email == "": 
            return None
        if not (re.fullmatch(regex, email)):
            self.__error = True
            st.warning("Email no valido") 

    def validate_empty_fields(self,user):
        """ Validar cuando hacen click espacios vacios
            y otros errores
        """
        #Revisar errores anteriores
        if self.__error:
            st.warning(f"Por favor corregir los errores mencionados") 
            return None

        #revisar espacios vacios
        for value in user.values():
            if not value:
                self.__error = True
                st.warning("Por favor llenar los campos solicitados") 
                break     
            
    @property
    def error(self):
        return self.__error



