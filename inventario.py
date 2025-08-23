"""Todas las funciones de el Menu Inventario se
manejan en este archivo"""

#Modulos Python
import os
import json
#Modulos Propios

#Modulos de terceros
import streamlit_tags as tgs
import streamlit as st
import pandas as pd

# Direccion json para el guardado de productos.
PATH_PRODUCTOS = 'catalogo_productos.json'

def entrada_al_catalogo(entrada:dict):
    """Esta funcion agregar entradas nuevas de inventario 
    en la base de datos catalogo de productos"""
    try:
        if os.path.exists(PATH_PRODUCTOS) and os.path.getsize(PATH_PRODUCTOS) > 0:
            
            with open(PATH_PRODUCTOS, 'r', encoding='utf-8') as l_file:               
                
                data = json.load(l_file)
                
                df_data = pd.DataFrame(data)
                df_entrada = pd.DataFrame(entrada)

                frames = [df_data, df_entrada]
                df_unido = pd.concat(frames)
                
                df_unido['Mascara'] = df_unido.duplicated(subset=['Producto','Dimension','U. Medida'])

                df_correcto = df_unido[df_unido['Mascara'] == False]
                df_incorrecto = df_unido[df_unido['Mascara'] == True]

                escritura_sin_duplicados = {
                    'Producto':df_correcto['Producto'].tolist(),
                    'Cantidad':df_correcto['Cantidad'].tolist(),
                    'Unidad':df_correcto['Unidad'].tolist(),
                    'Dimension':df_correcto['Dimension'].tolist(),
                    'U. Medida':df_correcto['U. Medida'].tolist(),
                    'Precio Compra':df_correcto['Precio Compra'].tolist(),
                    'Precio Venta':df_correcto['Precio Venta'].tolist()
                }

            with open(PATH_PRODUCTOS, 'w', encoding='utf-8') as e_file:
                
                json.dump(escritura_sin_duplicados, e_file, indent=4, ensure_ascii=False)
                
                existencia_de_incorrectos = df_incorrecto['Producto'].tolist()

                df_incorrecto = df_incorrecto.drop(['Mascara'], axis=1)
                
                if existencia_de_incorrectos:
                    duplicados_al_agregar = st.chat_message(name='human')
                    with duplicados_al_agregar:
                        st.write(':orange[LOS SIGUIENTES SON DATOS DUPLICADOS]')
                        st.dataframe(
                            df_incorrecto,
                            column_config={
                                'Precio Compra':st.column_config.NumberColumn(format='dollar', width=50),
                                'Precio Venta':st.column_config.NumberColumn(format='dollar',width=50)
                            }
                            )
                        return df_entrada
                else:
                    st.success('Datos Agregados con Exito')
                    return df_entrada
        else:
            
            with open(PATH_PRODUCTOS, 'w', encoding='utf-8') as ex_file:
                
                entrada_else = {
                    'Producto':entrada['Producto'],
                    'Cantidad':entrada['Cantidad'],
                    'Unidad':entrada['Unidad'],
                    'Dimension':entrada['Dimension'],
                    'U. Medida':entrada['U. Medida'],
                    'Precio Compra':entrada['Precio Compra'],
                    'Precio Venta':entrada['Precio Venta']
                }

                json.dump(entrada_else, ex_file, indent=4, ensure_ascii=False)
                exito_al_agregar = st.chat_message(name='human')
                with exito_al_agregar:
                    st.write('Datos Agregados')
                    df = pd.DataFrame(entrada_else)
                    return df
    
    except FileNotFoundError:
        
        with open(PATH_PRODUCTOS, 'w', encoding='utf-8') as c_file:
            
            creacion = {
                    'Producto':entrada['Producto'],
                    'Cantidad':entrada['Cantidad'],
                    'Unidad':entrada['Unidad'],
                    'Dimension':entrada['Dimension'],
                    'U. Medida':entrada['U. Medida'],
                    'Precio Compra':entrada['Precio Compra'],
                    'Precio Venta':entrada['Precio Venta']
                }
            
            json.dump(creacion, c_file, indent=4, ensure_ascii=False)
            exito_al_agregar = st.chat_message(name='human')
            with exito_al_agregar:
                st.write(':green[DATOS AGREGADOS CON EXITO]')
                df_creacion = pd.DataFrame(creacion)
                return df_creacion

def formulario_entrada_catalogo():
    
    st.write('__FORMULARIO DE ENTRADAS NUEVAS__')

    df = pd.DataFrame(
        {
            'Producto':[None],
            'Cantidad':[None],
            'Unidad':[None],
            'Dimension':[-1.00],
            'U. Medida':[None],
            'Precio Compra':[None],
            'Precio Venta':[None]
        }
    )
    
    opciones_seleccion_unidad = [
        'Pz (s)',
        'Bolsa (s)',
        'Paquete (s)',
        'Caja (s)'
        ]
    opciones_seleccion_unidad_medida = [
        'Kg (s)',
        'Lt (s)',
        'Mt (s)',
        'Mt (s) Cuadrado (s)',
        'Pulgada (s)',
        'Pz (s)',
        'Ninguno'
        ]
    
    df_editable = st.data_editor(
        df,
        key='dataframe_agregar',
        num_rows='dynamic',
        column_config={
            'Producto':st.column_config.TextColumn(
                width=150,
                help=':orange[Producto]',
                required=True,
                pinned=True,
                max_chars=100
            ),
            'Cantidad':st.column_config.NumberColumn(
                width=30,
                help=':orange[Cantidad]',
                required=True,
                default=0,
                min_value=0,
                step=1,
            ),
            'Unidad':st.column_config.SelectboxColumn(
                width=60,
                help=':orange[Unidad]',
                required=True,
                disabled=False,
                options=opciones_seleccion_unidad
            ),
            'Dimension':st.column_config.NumberColumn(
                width=40,
                help=':orange[Dimension] (Si el producto no tiene dimension ' \
                ':orange[agregar -1.00])',
                required=True,
                default=-1.00,
                min_value=-1.00,
                step=0.01
            ),
            'U. Medida':st.column_config.SelectboxColumn(
                width=90,
                help=':orange[U. Medida] ' \
                '(Si el producto no tiene U. Medida :orange[agregar "Ninguno"])',
                required=True,
                disabled=False,
                options=opciones_seleccion_unidad_medida
            ),
            'Precio Compra':st.column_config.NumberColumn(
                width=50,
                help=':orange[Precio Compra]',
                required=True,
                default=0.00,
                min_value=0.00,
                step=0.01,
                format='dollar'
            ),
            'Precio Venta':st.column_config.NumberColumn(
                width=50,
                help=':orange[Precio Venta]',
                required=True,
                default=1.00,
                min_value=0.00,
                step=0.01,
                format='dollar'
            )
        }
        )

    st.info(':material/lightbulb: Todos las nuevas entradas requieren un valor distinto de :red[None].\n' \
    'Todos los :red[Campos] son obligatorios, de lo contrario dicha fila no se guardara. Si dejas filas en blanco\n ' \
    'no se guardan.')

    agregar = st.button(label='Agregar', key='confirmar_entrada')
    
    if agregar:

        df_editable = df_editable.dropna()
        
        if  df_editable.empty == True:
            st.warning('Ingrese :red[Valores] en la :red[Tabla]')
            return
        
        else:

            df_editable['Producto'] = df_editable['Producto'].apply(lambda x: x.title().strip())
            df_compuesto = df_editable

            df_compuesto['Dimension'] = df_compuesto['Dimension'].astype('str')
            df_compuesto['Entrada'] = df_compuesto['Producto']+' '+df_compuesto['Dimension']+' '+df_compuesto['U. Medida']
            df_compuesto = df_compuesto.drop(['Producto', 'Dimension', 'U. Medida'], axis=1)
            
            orden_columnas = ['Entrada','Cantidad','Unidad','Precio Compra', 'Precio Venta']
            df_compuesto = df_compuesto.reindex(columns=orden_columnas)
            
            lista_repetidos = []
            df_compuesto['Mascara'] = df_compuesto['Entrada'].apply(lambda x: lista_repetidos.append(x) if x not in lista_repetidos else 1)
            df_compuesto = df_compuesto[df_compuesto['Mascara'] == 1]

            indices = df_compuesto.index

            df_editable = df_editable.drop(index=indices, axis=0)

            dict_cache = {
                'Producto':df_editable['Producto'].tolist(),
                'Cantidad':df_editable['Cantidad'].tolist(),
                'Unidad':df_editable['Unidad'].tolist(),
                'Dimension':df_editable['Dimension'].tolist(),
                'U. Medida':df_editable['U. Medida'].tolist(),
                'Precio Compra':df_editable['Precio Compra'].tolist(),
                'Precio Venta':df_editable['Precio Venta'].tolist()
            }
            
            df_exitos = entrada_al_catalogo(dict_cache)
            solicitud_de_entrada = st.chat_message(name='human')
            with solicitud_de_entrada:
                st.write(':green[TU SOLICITUD DE INGRESO:]')
                st.dataframe(
                    df_exitos,
                    column_config={
                        'Precio Compra':st.column_config.NumberColumn(format='dollar',width=50),
                        'Precio Venta':st.column_config.NumberColumn(format='dollar',width=50)
                    }
                    )
            st.page_link(label=':material/arrow_back: Volver A Inicio', page='inicio.py', use_container_width=True)
            return

def ver_inventario_completo():
    
    if os.path.exists(PATH_PRODUCTOS) and os.path.getsize(PATH_PRODUCTOS) > 0:
        
        with open(PATH_PRODUCTOS, 'r', encoding='utf-8') as lectura_file:
            
            datos = json.load(lectura_file)
            df = pd.DataFrame(datos)
            
            df_copia = df
            df_copia['Dimension'] = df_copia['Dimension'].astype('str')
            df_copia['Producto Y Modelo'] = df_copia['Producto'] + ' ' + df_copia['Dimension'] + ' ' + df_copia['U. Medida']
            df_copia = df_copia.drop(['Producto','Dimension','U. Medida'], axis=1)
            
            columnas_orden = ['Producto Y Modelo','Cantidad','Unidad','Precio Compra','Precio Venta']
            
            df_copia = df_copia.reindex(columns=columnas_orden)

            opciones_filtro = df_copia['Producto Y Modelo']

            filtro = st.multiselect(
                options=opciones_filtro,
                label='__BUSCAR PRODUCTOS__',
                key='filtro_buscar_productos',
            )
            
            if not filtro:
                return st.dataframe(
                    df_copia.sort_values(by='Producto Y Modelo', ascending=True).reset_index(drop=True),
                    column_config={
                        'Precio Compra':st.column_config.NumberColumn(format='dollar'),
                        'Precio Venta':st.column_config.NumberColumn(format='dollar')
                    }
                    )
            
            if filtro:
                df_consulta = df_copia[df_copia['Producto Y Modelo'].isin(filtro)]
                return st.dataframe(
                    df_consulta.sort_values(by='Producto Y Modelo', ascending=True).reset_index(drop=True),
                    column_config={
                        'Precio Compra':st.column_config.NumberColumn(format='dollar'),
                        'Precio Venta':st.column_config.NumberColumn(format='dollar')
                        }
                    )
    else:
        return st.info('No hay productos en el :orange["Inventario"]. ' \
        'Dirigite al sub-menu "Inventario/Agregar Producto"')

def ajustar_inventario():
    if os.path.exists(PATH_PRODUCTOS) and os.path.getsize(PATH_PRODUCTOS) > 0:
        
        with open(PATH_PRODUCTOS, 'r', encoding='utf-8') as file_edit:
            
            inventario_edit = json.load(file_edit)
            df = pd.DataFrame(inventario_edit)
            df_copia_simple = pd.DataFrame(inventario_edit)
            df['dimension_str'] = df['Dimension']
            df['dimension_str'] = df['dimension_str'].astype('str')
            df['Producto Y Modelo'] = df['Producto'] + ' ' + df['dimension_str'] + ' ' + df['U. Medida']
            opciones_nombres = df['Producto Y Modelo']
            filtro_ajuste = st.multiselect(
                label='__BUSCAR PRODUCTOS__',
                options=opciones_nombres,
                key='filtro_ajuste'
            )
            if filtro_ajuste:
                df_indice = df.set_index(df['Producto Y Modelo'])
                df_indice = df_indice[['Cantidad','Precio Compra','Precio Venta']]
                df_indice = df_indice[df_indice.index.isin(filtro_ajuste)]
                edited_df = st.data_editor(
                    df_indice.sort_index(),
                    disabled=['Producto y Modelo'],
                    column_config={
                        'Precio Compra':st.column_config.NumberColumn(format='dollar'),
                        'Precio Venta':st.column_config.NumberColumn(format='dollar')
                    }
                    )
                
                ajustes_cantidad = edited_df['Cantidad']
                ajustes_precio_compra = edited_df['Precio Compra']
                ajustes_precio_venta = edited_df['Precio Venta']
               
                indices_producto_modelo = edited_df.index

                df_seleccion = df[df['Producto Y Modelo'].isin(indices_producto_modelo)]
                
                indices_numericos = df_seleccion.index
                
                for ind1, cam1 in zip(indices_numericos, ajustes_cantidad):
                    df.loc[ind1, 'Cantidad'] = cam1
                for ind2, cam2 in zip(indices_numericos, ajustes_precio_compra):
                    df.loc[ind2, 'Precio Compra'] = cam2
                for ind3, cam3 in zip(indices_numericos, ajustes_precio_venta):
                    df.loc[ind3, 'Precio Venta'] = cam3
                
                guardar_ajustes = st.button(key='guardar_ajustes', label=':green[Guardar Ajustes]')
                
                if guardar_ajustes:

                    with open(PATH_PRODUCTOS, 'w', encoding='utf-8') as edicion_f:
                        
                        dict_editado = {
                            'Producto':df['Producto'].tolist(),
                            'Cantidad':df['Cantidad'].tolist(),
                            'Unidad':df['Unidad'].tolist(),
                            'Dimension':df['Dimension'].tolist(),
                            'U. Medida':df['U. Medida'].tolist(),
                            'Precio Compra':df['Precio Compra'].tolist(),
                            'Precio Venta':df['Precio Venta'].tolist()
                        }

                        json.dump(dict_editado, edicion_f, indent=4, ensure_ascii=False)             
                        exito_edicion = st.chat_message(name='human')
                        with exito_edicion:
                            st.write(':orange[__AJUSTES REALIZADOS__]')
                            st.dataframe(
                                df.loc[indices_numericos].drop(['Producto Y Modelo', 'dimension_str'], axis=1),
                                column_config={
                                    'Precio Compra':st.column_config.NumberColumn(format='dollar'),
                                    'Precio Venta':st.column_config.NumberColumn(format='dollar')
                                }
                                )
                            st.badge(color='green', label='Datos Guardados :material/check:')
                        st.page_link(label=':material/arrow_back: Volver A Inicio', page='inicio.py', use_container_width=True)
                        return
    else:
        return st.warning('No hay productos en el inventario')

def eliminar_entradas():

    if os.path.exists(PATH_PRODUCTOS) and  os.path.getsize(PATH_PRODUCTOS) > 0:

        with open(PATH_PRODUCTOS, 'r', encoding='utf-8') as l_file:

            datos = json.load(l_file)
            df = pd.DataFrame(datos)
            
            df['N. Dimension'] = df['Dimension']
            df['N. Dimension'] = df['N. Dimension'].astype('str')

            df['Producto Y Modelo'] = df['Producto']+' '+df['Dimension']+' '+df['U. Medida']

            opciones_seleccion = df['Producto Y Modelo']

            seleccion_eliminar = st.multiselect(
                key='seleccion_eliminar',
                label='__BUSCAR PRODUCTOS__',
                options=opciones_seleccion
            )

            if seleccion_eliminar:
                
                df_muestra = df[['Producto Y Modelo','Cantidad','Unidad','Precio Compra','Precio Venta']]
                st.dataframe(
                    df_muestra[df_muestra['Producto Y Modelo'].isin(seleccion_eliminar)],
                    column_config={
                        'Precio Compra':st.column_config.NumberColumn(format='dollar'),
                        'Precio Venta':st.column_config.NumberColumn(format='dollar')
                    }
                    )
                st.info(':material/lightbulb: Al dar click en :red[Eliminar] ' \
                'los cambios no pueden deshacercerse.')

                eliminar_seleccionados = st.button(
                    label=':red[:material/delete: Eliminar Seleccionados]',
                    key='eliminar_seleccionados'
                    )
                
                if eliminar_seleccionados:

                    df_muestra = df_muestra[df_muestra['Producto Y Modelo'].isin(seleccion_eliminar)]
                    indices = df_muestra.index
                    
                    df = df.drop(index=indices)
        
                    with open(PATH_PRODUCTOS, 'w', encoding='utf-8') as g_file:
                        
                        entradas_corregidas = {
                            'Producto':df['Producto'].tolist(),
                            'Cantidad':df['Cantidad'].tolist(),
                            'Unidad':df['Unidad'].tolist(),
                            'Dimension':df['Dimension'].tolist(),
                            'U. Medida':df['U. Medida'].tolist(),
                            'Precio Compra':df['Precio Compra'].tolist(),
                            'Precio Venta':df['Precio Venta'].tolist()
                        }
                        
                        json.dump(entradas_corregidas, g_file,indent=4, ensure_ascii=False)
                        
                        correcto_eliminar = st.chat_message(name='human')
                        
                        with correcto_eliminar:
                            st.write('Productos Eliminados Correcatamente')
                        
                        return st.page_link(
                            label=':material/arrow_back: Volver A Inicio',
                            page='inicio.py',
                            use_container_width=True
                            )
    
    else:
        st.warning('No hay datos en el :red[Inventario]')
        return
    
st.subheader(':material/inventory_2: Inventario - Menu')

seleccion_inventario_opciones = st.pills(
    key='agregar_entrada_al_inventario',
    label='',
    options=[
        ':material/inventory_2: Inventario',
        ':material/docs_add_on: Agregar Producto',
        ':material/table_edit: Ajustar Inventario',
        ':material/delete: Eliminar Producto'
        ],
    selection_mode='single',
    default=':material/inventory_2: Inventario',
    )

if seleccion_inventario_opciones == ':material/inventory_2: Inventario':
    ver_inventario_completo()    
    
if seleccion_inventario_opciones == ':material/docs_add_on: Agregar Producto':
    formulario_entrada_catalogo()

if seleccion_inventario_opciones == ':material/table_edit: Ajustar Inventario':
    ajustar_inventario()

if seleccion_inventario_opciones == ':material/delete: Eliminar Producto':
    eliminar_entradas()