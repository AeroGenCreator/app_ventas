import json

import lenguaje

from fpdf import FPDF
import streamlit as st
import pandas as pd

l=lenguaje.tu_idioma()

st.title(f':material/request_quote: {l.phrase[3]}')

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
        imprimir = st.button('Imprimir', type='secondary', width=200)

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

        class PDF(FPDF):
            def header(self):
                self.set_text_color(0,51,0)
                self.image('providencia_logo.jpeg', 10, 8, 16)
                self.set_font(family='helvetica', size=12, style='B')
                self.cell(20,6,txt='Ferreteria La Providecia: Cotizacion', border=False,ln=True, center=True,align='R')
                self.ln(15)
            def footer(self):
                self.set_y(-10)
                self.set_font('helvetica',style='I',size=9)
                self.cell(0,6,txt=f'Pagina {self.page_no()}/{{nb}}', center=True)
            
        # Creamos un nuevo objeto PDF
        pdf = PDF(orientation='portrait',unit='mm',format='Letter')

        # Inicializo el auto salto de pagina
        pdf.set_auto_page_break(auto=True, margin=10)

        pdf.add_page()
        pdf.set_font("Arial", size=10)
        pdf.set_line_width(0.1)
        pdf.set_draw_color(245,222,179)
        pdf.set_fill_color(245,222,179)#204,255,229
        pdf.set_text_color(0,51,0)

        pdf.cell(16,6,txt='Uni.',border=True,align='C') 
        pdf.cell(122,6,txt='Producto Y Modelo',border=True,align='C') 
        pdf.cell(29,6,txt='Precio U.',border=True,align='C') 
        pdf.cell(29,6,txt='Total', ln=True,border=True,align='C')
        
        pdf.cell(0,6,fill=True,ln=True)

        # Agrega los datos de la tabla (st.session_state.df)
        # Tendrás que iterar sobre las filas del DataFrame para agregar celdas al PDF
        for index, row in st.session_state.df.iterrows():
            pdf.cell(16,6,txt=f'{row['Unidades']}',border=True,align='C') 
            pdf.cell(122,6,txt=f'{row['Producto Y Modelo']}',border=True) 
            pdf.cell(29,6,txt=f'$ {row['Precio U.']}',border=True,align='R') 
            pdf.cell(29,6,txt=f'$ {row['Total']}', ln=True,border=True,align='R')

        half_page = (pdf.w / 2) - 10

        pdf.cell(0,6,fill=True,ln=True)
        pdf.cell(half_page,6,txt=f'Total de Productos: {st.session_state.productos}', border=True, align='C')
        pdf.cell(half_page,6,txt=f'Total De Cotizacion: $ {st.session_state.total}', border=True,align='C',ln=True)
        # Guarda el PDF en un archivo temporal
        pdf_output = bytes(pdf.output(dest='S'))
        
        # Proporciona el botón de descarga
        st.download_button(
            label="Descargar PDF",
            type='primary',
            data=pdf_output,
            file_name="cotizacion.pdf",
            mime="application/pdf",
            width=800
        )
