import yaml
from yaml.loader import SafeLoader
from pathlib import Path

import streamlit as st
import streamlit_authenticator as stauth

st.title('Titulo')

with open('credentials.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

try:
    login = authenticator.login(location='sidebar')
except Exception as e:
    st.error(e)



if st.session_state.get('authentication_status') is False:
    st.error('Username/password is incorrect')

if st.session_state.get('authentication_status') is None:
    st.warning('Please enter your username and password')

elif st.session_state.get('authentication_status'):
    authenticator.logout(location='sidebar', button_name='Cerrar Sesion')
    
    st.sidebar.subheader(f'Bienvenido :orange[{st.session_state.get('name')}]')
    
    iterable_pages = [
    st.Page(page='vender.py', title='Vender', icon=':material/sell:'),
    st.Page(page='inventario.py', title='Inventario', icon=':material/inventory_2:'),
    st.Page(page='presupuesto.py', title='Presupuesto', icon=':material/request_quote:'),
    st.Page(page='historial.py', title='Historial de Ventas', icon=':material/history:'),
    st.Page(page='estadisticas.py', title='Estadisticas', icon=':material/analytics:'),
    st.Page(page='config.py', title='Configuracion', icon=':material/settings:'),
    ]

    to_run = st.navigation(pages=iterable_pages, position='sidebar')

    to_run.run()


