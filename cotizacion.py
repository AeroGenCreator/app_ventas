import json

import lenguaje

from fpdf import FPDF
from fpdf.enums import TableCellFillMode
import streamlit as st
import pandas as pd

l=lenguaje.tu_idioma()

st.title(l.phrase[3])

RUTA_PRODUCTOS = 'catalogo_productos.json'


with open(RUTA_PRODUCTOS, 'r', encoding='utf-8') as file:
    datos = json.load(file)
    df = pd.DataFrame(data=datos)
    df['Precio Venta'] = round(df['Precio Venta'])
    df['Precio Unitario'] = df['Precio Venta']
    df['Precio Unitario'] = df['Precio Unitario'].astype('str')
    df['Producto Y Modelo'] = df['Producto']+' '+df['Dimension']+' '+df['U. Medida']
    df = df.set_index('Producto Y Modelo',drop=True)
    
    OPCIONES = df.index
    
    DF_VACIO = pd.DataFrame(
        {
        'Unidades':[None],
        'Producto Y Modelo':[None],
        'Precio U.':[None],
        'Total':[None],
        'Existencias':[None]
        }
    )

    cotizacion_total = 0
    productos_en_cotizacion = 0

    if 'df' not in st.session_state:
        st.session_state.df = DF_VACIO
    if 'total'not in st.session_state:
        st.session_state.total = cotizacion_total
    if 'productos' not in st.session_state:
        st.session_state.productos = productos_en_cotizacion
    
    edicion = st.data_editor(
        data=st.session_state.df,
        key='editor_cotizacion',
        num_rows='dynamic',
        column_order=['Unidades', 'Producto Y Modelo','Precio U.' ,'Total','Existencias'],
        hide_index=True,
        column_config={
            'Unidades':st.column_config.NumberColumn(disabled=False,width=50,help=':orange[Unidades]',step=1),
            'Producto Y Modelo':st.column_config.SelectboxColumn(options=OPCIONES,width=400,help=':orange[Producto Y Modelo]'),
            'Precio U.':st.column_config.NumberColumn(format='dollar', disabled=True, width=50, help=':orange[Precio Unitario]'),
            'Total':st.column_config.NumberColumn(disabled=True,width=50, format='dollar',help=':orange[Total]'),
            'Existencias':st.column_config.TextColumn(disabled=True, width=60,help=':orange[Existencias]')
        }
    )
    
    metric1,metric2 = st.columns([2,2])
    metric1.metric('Productos en la Cotizacion', value=st.session_state.productos,border=True)
    metric2.metric('Precio Total Cotizacion',value=st.session_state.total, border=True)

    edicion = pd.DataFrame(edicion)

    col1, col2, col3 = st.columns(3)
    with col1:
        calcular_total = st.button('Calcular Total',width=200)
    with col2:
        limpiar_tabla = st.button('Limpiar Tabla',width=200)
    with col3:
        imprimir = st.button('Imprimir', type='primary', width=200)

    if edicion.empty:
        del st.session_state.df
        del st.session_state.total
        del st.session_state.productos

    if limpiar_tabla:
        try:
            st.session_state.df = DF_VACIO
            st.session_state.total = cotizacion_total
            st.session_state.productos = productos_en_cotizacion
        except(KeyError):
            if 'df' not in st.session_state:
                st.session_state.df = DF_VACIO
            if 'total' not in st.session_state:
                st.session_state.total = cotizacion_total
            if 'productos' not in st.session_state:
                st.session_state.productos = productos_en_cotizacion

    if calcular_total:
        edicion = edicion.dropna(axis=0,how='any',subset='Producto Y Modelo')
        edicion = edicion.drop_duplicates(subset='Producto Y Modelo')
        if edicion.empty:
            st.session_state.df = DF_VACIO
        else:
            linker = df.loc[edicion['Producto Y Modelo']]
            
            union = pd.merge(
                edicion,
                linker,
                how='left',
                on='Producto Y Modelo'
                )
            
            union['Precio Venta'] = round(union['Precio Venta'])
            union['Precio U.'] = union['Precio Venta']
            union['Total'] = union['Unidades'] * union['Precio Venta']
            union['Existencias'] = union['Cantidad']

            union = union.reindex(columns=['Unidades','Producto Y Modelo','Precio U.','Total','Existencias'])
            
            cotizacion_total += union['Total'].sum()
            productos_en_cotizacion += union['Unidades'].sum()

            st.session_state.productos = productos_en_cotizacion
            st.session_state.total = cotizacion_total
            st.session_state.df = union
    
    if imprimir:

        # Creamos un nuevo objeto PDF
        pdf = FPDF(orientation='portrait',unit='mm',format='Letter')
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Agrega el título
        pdf.cell(200, 10, txt="COTIZACION", ln=True, markdown=True)
        pdf.cell(0,6,fill=True,ln=True)

        # Agrega los datos de la tabla (st.session_state.df)
        # Tendrás que iterar sobre las filas del DataFrame para agregar celdas al PDF
        for index, row in st.session_state.df.iterrows():
            pdf.cell(
                0,
                6,
                txt=f'- {row['Unidades']} {row['Producto Y Modelo']} - $ {row['Precio U.']} - $ {row['Total']}',
                border=True,
                ln=True
                )
            
        pdf.cell(0,6,fill=True,ln=True)
        pdf.cell(0,6,txt=f'Total de Productos: {st.session_state.productos}', border=True,ln=True)
        pdf.cell(0,6,fill=True,ln=True)
        pdf.cell(0,6,txt=f'Total De Cotizacion: $ {st.session_state.total}', border=True,ln=True)
        # Guarda el PDF en un archivo temporal
        pdf_output = bytes(pdf.output(dest='S'))
        
        # Proporciona el botón de descarga
        st.download_button(
            label="Descargar PDF",
            data=pdf_output,
            file_name="cotizacion.pdf",
            mime="application/pdf"
        )
