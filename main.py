import streamlit as st
from Form.Validators import Validators
from data.data import UNIVERSIDADES,PODIO_REFERRAL,BACKGROUNDS

validate = Validators()
container = st.empty()

with container.container():
    st.title('Registrarse')
    st.caption('Programa de pasantias y voluntariado con AIESEC')

    first_name = st.text_input("First name")
    last_name = st.text_input("Last Name")
    
    email = st.text_input("Email")
    validate.validate_email(email) #Validar el email, ver metodos en Form/Validators

    password = st.text_input("Password",type="password")
    validate.validate_password(password) #Validar el password, ver metodos en Form/Validators

    phone = st.text_input("Phone number")

    #Ingresar universidad. La data es traida directamente de EXPA. esta está en data/data.py
    universidad = st.selectbox('Universidad', UNIVERSIDADES,index=len(UNIVERSIDADES)-1)
    background = st.selectbox('Carrera o Background profesional', BACKGROUNDS,index=len(BACKGROUNDS)-1)

    #Ingresar referral. La data es traida directamente de EXPA. esta está en data/data.py
    referrals = st.selectbox( label='Referral',options=list(PODIO_REFERRAL.keys()),index=len(list(PODIO_REFERRAL.keys()))-1)
    
    #Creamos un diccionario llamado usuario con todos los valores
    user = {"First Name":first_name,"Last Name":last_name,"Email":email,"Password":password,"Phone":phone,"Universidad":universidad,'Background':background,"Referral":referrals}

    #Registrarse. El boton es un bool (True or False)
    btn = st.button("Registrarse")


if btn: 
    response = validate.register(user)
    if response == "Registro Exitoso":
        container.empty()
        st.title("Te has registrado de manera exitosa!")
        st.markdown("Puedes ingresar a tu cuenta en **[aiesec.org](https://auth.aiesec.org/users/sign_in?country=)**")
        st.caption("Debes ser contactad@ en las proximas 48h")








