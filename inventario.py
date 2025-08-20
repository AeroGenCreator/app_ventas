import streamlit_tags as tgs
import streamlit as st
import os
import json
import pandas as pd

PATH_PRODUCTOS = 'catalogo_productos.json'

def entrada_al_catalogo(entrada:list):
    """Esta funcion agregar entradas nuevas de inventario 
    en la base de datos catalogo de productos"""
    try:
        if os.path.exists(PATH_PRODUCTOS) and os.path.getsize(PATH_PRODUCTOS) > 0:
            
            with open(PATH_PRODUCTOS, 'r', encoding='utf-8') as l_file:               
                catalogo_productos = json.load(l_file)

                if entrada[0] in catalogo_productos['nombre'] and entrada[3] in catalogo_productos['dimension']:
                    st.warning(f'El producto :red["{entrada[0]} {entrada[3]} {entrada[4]}"] ya fue agregado. Si deseas eliminarlo dirigete al sub-menu "Inventario/Eliminar Entrada". Si deseas editarlo o ajustarlo, dirigete al sub_menu "Inventario/Ajustes"')
                    return
                
                else:

                    catalogo_productos['nombre'].append(entrada[0])
                    catalogo_productos['cantidad'].append(entrada[1])
                    catalogo_productos['unidad'].append(entrada[2])
                    catalogo_productos['dimension'].append(entrada[3])
                    catalogo_productos['u_de_medida'].append(entrada[4])
                    catalogo_productos['precio_compra'].append(entrada[5])
                    catalogo_productos['precio_catalogo'].append(entrada[6])
                    catalogo_productos['valor_bruto'].append(entrada[7])
                    catalogo_productos['margen_ingreso'].append(entrada[8])

            with open(PATH_PRODUCTOS, 'w', encoding='utf-8') as e_file:
                json.dump(catalogo_productos, e_file, indent=4, ensure_ascii=False)
                exito_al_agregar = st.chat_message(name='human')
                with exito_al_agregar:
                    st.write('Nuevo Producto Agregado')
                    return
        else:
            with open(PATH_PRODUCTOS, 'w', encoding='utf-8') as ex_file:
                creacion_else = {
                    'nombre':[entrada[0]],
                    'cantidad':[entrada[1]],
                    'unidad':[entrada[2]],
                    'dimension':[entrada[3]],
                    'u_de_medida':[entrada[4]],
                    'precio_compra':[entrada[5]],
                    'precio_catalogo':[entrada[6]],
                    'valor_bruto':[entrada[7]],
                    'margen_ingreso':[entrada[8]],
                }

                json.dump(creacion_else, ex_file, indent=4, ensure_ascii=False)
                exito_al_agregar = st.chat_message(name='human')
                with exito_al_agregar:
                    st.write('Nuevo Producto Agregado')
                    return
    
    except FileNotFoundError:
        with open(PATH_PRODUCTOS, 'w', encoding='utf-8') as c_file:
            creacion = {
                'nombre':[entrada[0]],
                'cantidad':[entrada[1]],
                'unidad':[entrada[2]],
                'dimension':[entrada[3]],
                'u_de_medida':[entrada[4]],
                'precio_compra':[entrada[5]],
                'precio_catalogo':[entrada[6]],
                'valor_bruto':[entrada[7]],
                'margen_ingreso':[entrada[8]],
            }

            json.dump(creacion, c_file, indent=4, ensure_ascii=False)
            exito_al_agregar = st.chat_message(name='human')
            with exito_al_agregar:
                st.write('Nuevo Producto Agregado')
                return

def formulario_entrada_catalogo():
    en1, en2, en3 = st.columns(3)
    with en1:
        nombre = st.text_input(key='entrada_nombre', label='Nombre de Producto')
        try:
            nombre = nombre.strip().title()
        except AttributeError:
            nombre
    with en2:
        cantidad = st.number_input(key='entrada_cantidad', label='Cantidad', step=1, min_value=1)
    with en3:
        unidad_pieza = st.selectbox(key='entrada_unidad_pieza', label='Unidad', options=['Pz (s)', 'Bolsa (s)', 'Caja (s)', 'Empaque (s)'])
    
    en4, en5, en6, en7 = st.columns(4)
    with en4:
        dimension = st.number_input(key='entrada_dimension', label='Dimension', min_value=0.0, step=0.1)
    with en5:
        unidad = st.selectbox(key='entrada_unidad', label='Unidad De Medida',options=['Kg', 'Lt', 'Mt', 'Mt-Cuadrado', 'Pulgada (s)', 'Pz (s)'])
    with en6:
        precio_adquisicion = st.number_input(key='entrada_precio_ad', label='Precio De Compra')
    with en7:
        precio_catalogo = st.number_input(key='entrada_precio_cat', label='Precio De Venta', min_value=1.0)

    valor_bruto = precio_catalogo * cantidad
    if precio_catalogo > precio_adquisicion:
        diferencia = precio_catalogo - precio_adquisicion
        margen_ingreso = diferencia * cantidad    
        
        lista_cache = [
        nombre,
        cantidad,
        unidad_pieza,
        dimension,
        unidad,
        precio_adquisicion,
        precio_catalogo,
        valor_bruto,
        margen_ingreso
        ]
    
        df = pd.DataFrame(
        data=lista_cache,
        index=[
            'Producto',
            'Cantidad',
            'Unidad',
            'Dimension',
            'Unidad de Medida',
            'Precio de Compra',
            'Precio de Venta',
            'Valor Bruto',
            'Margen de Ingreso'
        ],
        columns=['Nueva Entrada de Producto']
        )
    
        st.dataframe(df)
    
        agregar = st.button(label='Agregar', key='confirmar_entrada')
        if agregar:
            entrada_al_catalogo(lista_cache)
    else:
        st.warning('Tu "Margen de ingreso" es negativo o igual a cero,' \
        ' Tu :red["Precio de adquisicion"] debe ser menor que tu :red["Precio de catalogo"]')

def ver_inventario_completo():
    if os.path.exists(PATH_PRODUCTOS) and os.path.getsize(PATH_PRODUCTOS) > 0:
        with open(PATH_PRODUCTOS, 'r', encoding='utf-8') as lectura_file:
            inventario_completo = json.load(lectura_file)
            
            opciones_filtro = inventario_completo['nombre']
            
            df = pd.DataFrame(inventario_completo)
            
            filtro = tgs.st_tags(
                suggestions=opciones_filtro,
                label='Buscar Producto',
                text='Enter Para Mas Productos A La Busqueda',
                key='filtro_buscar_productos'
            )
            
            if not filtro:
                st.dataframe(df.sort_values(by=['nombre'], ascending=False).reset_index(drop=True))
            
            if filtro:
                
                filtro_corregido = []
                
                for e in filtro:
                    try:
                        e = e.strip(). title()
                        filtro_corregido.append(e)
                    except AttributeError:
                        filtro_corregido.append(e)

                df_consulta = df[df['nombre'].isin(filtro_corregido)]
                st.dataframe(df_consulta)
    else:
        st.info('No hay productos en el :red["Inventario"]. ' \
        'Dirigite al sub-menu "Inventario/Agregar Producto"')
        st.write('')

seleccion_inventario_opciones = st.pills(
    key='agregar_entrada_al_inventario',
    label='Opciones De Inventario',
    options=[
        ':material/inventory_2: Inventario',
        ':material/docs_add_on: Agregar Producto'],
    selection_mode='single',
    default=':material/inventory_2: Inventario',
    )

if seleccion_inventario_opciones == ':material/inventory_2: Inventario':
    ver_inventario_completo()    
    
if seleccion_inventario_opciones == ':material/docs_add_on: Agregar Producto':
    formulario_entrada_catalogo()