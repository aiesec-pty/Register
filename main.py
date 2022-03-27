from operator import index
import streamlit as st
#Validación de passwords y emails 
from utils.Validators import Validators
#Data de universidades de Expa, Backgrounds de Expa, Referrals de EXPA e IDs de Podio
from utils.data import UNIVERSIDADES,PODIO_REFERENTES,BACKGROUNDS_SPANISH,NIVEL_INGLES,ESTUDIOS
from utils.Register import Register

validate = Validators() #Instancia de validator (Valida email y password)
container = st.empty()

with container.container():
    st.title('Registrarse')
    st.caption('Programa de pasantias y voluntariados con AIESEC')

    st.subheader("Información Básica")
    first_name = st.text_input("Nombre")
    last_name = st.text_input("Apellido")
    edad = st.text_input("Edad")
    email = st.text_input("Email");validate.validate_email(email)
    phone = st.text_input("Numero de celular")
    password = st.text_input("Contraseña",type="password",help="Contraseña para tu cuenta de AIESEC.org");validate.validate_password(password) 
    referrals = st.selectbox(label='¿Como te enteraste de nosotros?',options=list(PODIO_REFERENTES.keys()),index=len(list(PODIO_REFERENTES.keys()))-1,)

    st.subheader("Información Profesional")
    universidad = st.selectbox('Universidad', UNIVERSIDADES,index=len(UNIVERSIDADES)-1)
    background = st.selectbox('Carrera o Background profesional', BACKGROUNDS_SPANISH,index=len(BACKGROUNDS_SPANISH)-1)
    ingles = st.selectbox(label="Nivel de Ingles",options=list(NIVEL_INGLES.keys()),index=len(list(NIVEL_INGLES.keys()))-1)
    estudios = st.selectbox(label="Estudios",options=list(ESTUDIOS.keys()),index=len(list(ESTUDIOS.keys()))-1)
    #cv = st.file_uploader("Hoja de vida o CV (pdf)",type="pdf")


    #Creamos un diccionario llamado usuario con todos los valores
    user = {
        "First Name":first_name,"Last Name":last_name,
        "Email":email,"Password":password,
        "Phone":phone,"Universidad":universidad,
        'Background':background,"Referral":referrals,
        "Edad":edad,"Ingles":ingles,"Estudios":estudios
    }

    #Registrarse. El boton es un bool (True or False)
    btn = st.button("Registrarse")


if btn: 
    validate.validate_empty_fields(user)
    if not validate.error:
        register = Register(user)
        response = register.expa_register()
        response_dict = dict(response.json()) 

        #Si el registro fue incorrecto, aiesec.org retorna un response
        #con errors. Revisamos si este fue el caso con el siguiente código.
        #En caso tal de que no, registramos en Podio
        
        if 'errors' in response_dict.keys():
            for error, message in response_dict['errors'].items():
                st.warning(f'{error.capitalize()} {message[0]}')
        else:
            register.podio_register()
            container.empty()
            st.balloons()
            st.title("Te has registrado de manera exitosa!")
            st.markdown("Puedes ingresar a tu cuenta en **[aiesec.org](https://auth.aiesec.org/users/sign_in?country=)**")
            st.caption("Debes ser contactad@ en las proximas 48h") 








