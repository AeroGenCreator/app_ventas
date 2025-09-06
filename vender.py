import datetime
import json
import os

import lenguaje

import streamlit as st
import pandas as pd

l=lenguaje.tu_idioma()

st.title(f':material/sell: {l.phrase[1]}')

RUTA_HISTORIAL = 'ventas_historial.json'
RUTA_PRODUCTOS = 'catalogo_productos.json'

SALES_EMPTY_DICT = {
    'Folio':[],
    'Fecha':[],
    'Clave SAT':[],
    'Producto Y Modelo':[],
    'Cantidad':[],
    'Unidad':[],
    'Precio':[],
    'Total':[]
    }

CODIGO_QR = 'Cero'

def acceso_a_historial():
    try:
        if os.path.exists(RUTA_HISTORIAL) and os.path.getsize(RUTA_HISTORIAL) > 0:
            with open(RUTA_HISTORIAL,'r',encoding='utf-8') as f:
                data = json.load(f)
                return data
        else:
            with open(RUTA_HISTORIAL, 'w', encoding='utf-8') as f:
                json.dump(SALES_EMPTY_DICT, f, indent=4, ensure_ascii=False)

    except(FileNotFoundError, json.JSONDecodeError, TypeError):
        st.error('Error Al Acceder Al Historial De Ventas')

def get_folio(data:dict):

    df = pd.DataFrame(data=data)

    folio = df['Folio']
    folio = sorted(folio,reverse=True)

    if len(folio) > 0:
        folio = folio[0]
        folio += 1
        return folio
    else:
        return 0

def acceso_a_productos():
    try:
        if os.path.exists(RUTA_PRODUCTOS) and os.path.getsize(RUTA_PRODUCTOS) > 0:
            with open(RUTA_PRODUCTOS, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        else:
            st.warning('O El Archivo No Existe O No Hay Datos En El Inventario')
    except(FileNotFoundError):
        st.error('Error Al Acceder Al Historial De Ventas')

def formulario_venta(folio:int, data:dict):

    df=pd.DataFrame(data=data)
    df['Producto Y Modelo']=df['Producto']+df['Dimension']+df['U. Medida']
    df['Precio Venta']=round(df['Precio Venta'])
    df=df.set_index(keys='Producto Y Modelo',drop=True)

    OPCIONES = df.index.to_list()

    DF_VACIO = {
        'Cantidad':[None],
        'Producto Y Modelo':[None],
        'Unidad':[None],
        'Clave SAT':[None],
        'Precio':[None],
        'Total':[None],
        'Existencias':None,
        'Faltas':[None]
    }
    
    if 'df' not in st.session_state:
        st.session_state.df = DF_VACIO

    dt = datetime.date.today()

    st.write('Ignacio Picazo Sur No. 30 Santa Ana Chiautempan, Tlaxcala C.P. 90800')

    col_1, col_2, col_3 = st.columns(3)
    col_1.write(':red[__NOTA DE VENTA__]')
    col_2.write(dt)
    col_3.write(f'__No. Folio: :red[{folio}]__')

    venta = st.data_editor(
        data=st.session_state.df,
        column_config={
            'Cantidad':st.column_config.NumberColumn(
                width=80,
                help=':orange[Cantidad]',
                required=True,
                pinned=True,
                min_value=1,
                step=1
            ),
            'Producto Y Modelo':st.column_config.SelectboxColumn(
                width=200,
                help=':orange[Producto Y Modelo]',
                required=True,
                pinned=True,
                options=OPCIONES,
                ),
            'Unidad':st.column_config.TextColumn(
                width=60,
                help=':orange[Unidad]',
                disabled=True,
                pinned=True,
            ),
            'Clave SAT':st.column_config.TextColumn(
                width=90,
                help=':orange[Clave SAT]',
                disabled=True,
                pinned=True
            ),
            'Precio':st.column_config.NumberColumn(
                width=75,
                help=':orange[Precio]',
                disabled=True,
                pinned=True,
                format='dollar',
            ),
            'Total':st.column_config.NumberColumn(
                width=75,
                help=':orange[Total]',
                disabled=True,
                pinned=True,
                format='dollar'
            ),
            'Existencias':st.column_config.NumberColumn(
                width=70,
                help=':orange[Existencias]',
                disabled=True,
                pinned=True,
            ),
            'Faltas':st.column_config.TextColumn(
                width=50,
                help=':orange[Faltas]',
                disabled=True,
                pinned=True,
            )
        }
    )

    limpiar_tabla = st.button(
        label='Limpiar Tabla',
        key='reset_tabla',
        type='secondary',
        help=':orange[Requiere Doble Click]',
        width=800
        )
    
    if limpiar_tabla:
        st.session_state.df=DF_VACIO


# SEPARACION --------------------------------------------------------------------------------------------------

historial = acceso_a_historial()
folio = get_folio(historial)
productos = acceso_a_productos()
formulario_venta(folio=folio,data=productos)

st.dataframe(historial)