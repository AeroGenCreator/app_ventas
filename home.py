import streamlit as st


b = st.button('press')
if not b:
    st.write('user, antes que nada para acceder a los menus')
else:
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