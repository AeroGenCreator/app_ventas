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
                    'precio_catalogo':[entrada[6]]
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
                'precio_catalogo':[entrada[6]]
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
        dimension = st.number_input(key='entrada_dimension', label='Dimension', min_value=0.0, step=1.0)
    with en5:
        unidad = st.selectbox(key='entrada_unidad', label='Unidad De Medida',options=['Kg', 'Lt', 'Mt', 'Mt-Cuadrado', 'Pulgada (s)', 'Pz (s)', 'Ninguno'])
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
            st.page_link(label=':material/arrow_back: Volver A Inicio', page='inicio.py', use_container_width=True)
            return
    else:
        st.warning('Tu "Margen de ingreso" es negativo o igual a cero,' \
        ' Tu :red["Precio de adquisicion"] debe ser menor que tu :red["Precio de catalogo"]')

def ver_inventario_completo():
    if os.path.exists(PATH_PRODUCTOS) and os.path.getsize(PATH_PRODUCTOS) > 0:
        with open(PATH_PRODUCTOS, 'r', encoding='utf-8') as lectura_file:
            inventario_completo = json.load(lectura_file)
            
            opciones_filtro = inventario_completo['nombre']
            
            df = pd.DataFrame(inventario_completo)
            
            filtro = st.multiselect(
                options=opciones_filtro,
                label='Buscar Producto',
                key='filtro_buscar_productos',
            )
            
            if not filtro:
                st.dataframe(df.sort_values(by=['nombre'], ascending=False).reset_index(drop=True))
            
            if filtro:
                df_consulta = df[df['nombre'].isin(filtro)]
                st.dataframe(df_consulta)
    else:
        st.info('No hay productos en el :red["Inventario"]. ' \
        'Dirigite al sub-menu "Inventario/Agregar Producto"')
        st.write('')

def ajustar_inventario():
    if os.path.exists(PATH_PRODUCTOS) and os.path.getsize(PATH_PRODUCTOS) > 0:
        with open(PATH_PRODUCTOS, 'r', encoding='utf-8') as file_edit:
            inventario_edit = json.load(file_edit)
            df = pd.DataFrame(inventario_edit)
            df_copia_simple = pd.DataFrame(inventario_edit)
            df['dimension_str'] = df['dimension']
            df['dimension_str'] = df['dimension_str'].astype('str')
            df['nombre_compuesto'] = df['nombre'] + ' ' + df['dimension_str'] + ' ' + df['u_de_medida']
            opciones_nombres = df['nombre_compuesto']
            filtro_ajuste = st.multiselect(
                label='Buscar Productos',
                options=opciones_nombres,
                key='filtro_ajuste'
            )
            if filtro_ajuste:
                df_indice = df.set_index(df['nombre_compuesto'])
                df_indice = df_indice[['cantidad','precio_compra','precio_catalogo']]
                df_indice = df_indice[df_indice.index.isin(filtro_ajuste)]
                edited_df = st.data_editor(df_indice.sort_index(), disabled=['nombre_compuesto'])
                
                ajustes_cantidad = edited_df['cantidad']
                ajustes_precio_compra = edited_df['precio_compra']
                ajustes_precio_catalogo = edited_df['precio_catalogo']
                indices_nombre_compuesto = edited_df.index
                df_seleccion = df[df['nombre_compuesto'].isin(indices_nombre_compuesto)]
                indices_numericos = df_seleccion.index
                for ind1, cam1 in zip(indices_numericos, ajustes_cantidad):
                    df.loc[ind1, 'cantidad'] = cam1
                for ind2, cam2 in zip(indices_numericos, ajustes_precio_compra):
                    df.loc[ind2, 'precio_compra'] = cam2
                for ind3, cam3 in zip(indices_numericos, ajustes_precio_catalogo):
                    df.loc[ind3, 'precio_catalogo'] = cam3
                st.write('Antes del Ajuste')
                st.dataframe(df_copia_simple.loc[indices_numericos])
                st.write('Despues del Ajuste')
                st.dataframe(df.loc[indices_numericos].drop(['nombre_compuesto', 'dimension_str'], axis=1))
                
                guardar_ajustes = st.button(key='guardar_ajustes', label='Guardar Ajustes')
                if guardar_ajustes:
                    nombre_ed = df['nombre']
                    cantidad_ed = df['cantidad']
                    unidad_ed = df['unidad']
                    dimension_ed = df['dimension']
                    u_de_medida_ed = df['u_de_medida']
                    precio_compra_ed = df['precio_compra']
                    precio_catalogo = df['precio_catalogo']

                    with open(PATH_PRODUCTOS, 'w', encoding='utf-8') as edicion_f:
                        dict_editado = {
                            'nombre': nombre_ed.tolist(),
                            'cantidad': cantidad_ed.tolist(),
                            'unidad': unidad_ed.tolist(),
                            'dimension': dimension_ed.tolist(),
                            'u_de_medida': u_de_medida_ed.tolist(),
                            'precio_compra': precio_compra_ed.tolist(),
                            'precio_catalogo': precio_catalogo.tolist()
                        }
                        json.dump(dict_editado, edicion_f, indent=4, ensure_ascii=False)             
                        st.write('Exito')
                        st.page_link(label=':material/arrow_back: Volver A Inicio', page='inicio.py', use_container_width=True)
                        return
    else:        
        return st.warning('No hay productos en el inventario')

st.subheader('Opciones de Inventario')
seleccion_inventario_opciones = st.pills(
    key='agregar_entrada_al_inventario',
    label='',
    options=[
        ':material/inventory_2: Inventario',
        ':material/docs_add_on: Agregar Producto',
        ':material/table_edit: Ajustar Inventario'
        ],
    selection_mode='single',
    default=':material/inventory_2: Inventario',
    )

if seleccion_inventario_opciones == ':material/inventory_2: Inventario':
    ver_inventario_completo()    
    
if seleccion_inventario_opciones == ':material/docs_add_on: Agregar Producto':
    formulario_entrada_catalogo()

if seleccion_inventario_opciones == ':material/table_edit: Ajustar Inventario':
    st.write('En Construccion')
    ajustar_inventario()