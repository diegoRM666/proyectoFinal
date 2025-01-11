import streamlit as st
import pandas as pd
import logic.bd as bd
import logic.utilities as ut
from menu import menu_with_redirect
import plotly.graph_objects as go
import plotly.express as px
from pylatex import Document, Section, Figure, NoEscape, Subsection
import os

# Comprueba que el usuario este loggeado.
menu_with_redirect()

# Título de la pagina
st.markdown("# 📊 Generación de Reportes")

# Se generan columnas para el despliegue con formato en la pagina
col1, col2 = st.columns([8, 2])
with col2:
    # Selector de rango para el calculo de los reportes
    range_selected = st.selectbox("Rango", ["1 Semana", "1 Mes", "6 Meses"])

# Permite obtener el directorio actual del proyecto
current_directory = os.getcwd()
# Con base en el rango de fechas obtiene la fecha de inicio y de fin del rango
end_date, start_date = ut.date_report(range_selected) 

# Genera las rutas absolutas para las imagenenes y un formato estandar para los nombres
semipath_name = f"{start_date}_to_{end_date}"
semi_path_img = current_directory + f"/reports/img/"


# Lista para almacenar imágenes de gráficas y sus títulos
image_files = []

# Gráfica: Actividades cerradas y abiertas
# Consulta las actividades cerradas y abiertas en un rango de fechas
activities_closed, activities_open, avg_solved = bd.consultar_actividades_report(start_date, end_date)
# Comprueba que el resultado no sea vacio
if activities_closed is not None  and activities_open is not None:
    # Calculo de altura de las tablas, esto para darle formato
    num_filas = len(activities_closed)
    num_filas2 = len(activities_open)

    st.markdown("## Actividades Cerradas y Abiertas")
    # Generacion de una grafica de tiempo
    fig_pol1 = go.Figure()

    # Agrega el trazado para las actividades cerradas
    fig_pol1.add_trace(go.Scatter(
        x=activities_closed['fecha_cierre'],
        y=activities_closed['actividades_cerradas'],
        mode='lines+markers',
        name='Cerradas',
        line=dict(color=px.colors.sequential.RdBu[0]) # Se utilizo un esquema de colores predeterminados
    ))

    # Agrega el trazado para las actividades abiertas en el mismo grafico
    fig_pol1.add_trace(go.Scatter(
        x=activities_open['fecha_apertura'],
        y=activities_open['actividades_abiertas'],
        mode='lines+markers',
        name='Abiertas',
        line=dict(color=px.colors.sequential.RdBu_r[0])
    ))

    # Actualiza la grafica, especificando los titulos de ejes y la transparencia
    fig_pol1.update_layout(
        xaxis_title="Fecha",
        yaxis_title="Actividades",
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)'
    )

    # Genera una tabla para las actividades cerradas
    table_act_close = go.Figure(
        go.Table(
            header=dict(
                values=["Fecha Cierre", "Actividades Cerradas"],  # Títulos de las columnas
                font=dict(color='white'),  # Color del texto del encabezado
                fill_color=px.colors.sequential.RdBu[0]  # Usamos el primer color de la paleta para el encabezado
            ),
            cells=dict(
                values=[
                    activities_closed[activities_closed.columns[1]],  # Valores de la primera columna
                    activities_closed[activities_closed.columns[0]]   # Valores de la segunda columna
                ],
                font=dict(color='white'),  # Color del texto de las celdas
                fill_color=[px.colors.sequential.RdBu[2], px.colors.sequential.RdBu[2]]  # Aplicar dos colores alternados para las columnas
            )
        )
    )

    # Actualiza la tabla para darle la altura precisa
    table_act_close.update_layout(
        height=ut.det_height_table(num_filas),
        margin=dict(l=0, r=0, t=0, b=0),  # Eliminar los márgenes (izquierda, derecha, arriba y abajo)
        paper_bgcolor='rgba(0,0,0,0)'  # Hacer el fondo transparente
    )
    
    # Genera una tabla para las actividades abiertas
    table_act_open = go.Figure(
        go.Table(
            header=dict(
                values=["Fecha Apertura", "Actividades Abiertas"],  # Títulos de las columnas
                font=dict(color='white'),  # Color del texto del encabezado
                fill_color=px.colors.sequential.RdBu[0]  # Usamos el primer color de la paleta para el encabezado
            ),
            cells=dict(
                values=[
                    activities_open[activities_open.columns[1]],  # Valores de la primera columna
                    activities_open[activities_open.columns[0]]   # Valores de la segunda columna
                ],
                font=dict(color='white'),  # Color del texto de las celdas
                fill_color=[px.colors.sequential.RdBu[2], px.colors.sequential.RdBu[2]]  # Aplicar dos colores alternados para las columnas
            )
        )
    )

    # Actualiza la tabla para darle la altura precisa
    table_act_open.update_layout(
        height=ut.det_height_table(num_filas2),
        margin=dict(l=0, r=0, t=0, b=0),  # Eliminar los márgenes (izquierda, derecha, arriba y abajo)
        paper_bgcolor='rgba(0,0,0,0)'  # Hacer el fondo transparente
    )

    # Se despliega la figura que contiene las actividades cerradas y abiertas en el total de la pagina
    st.plotly_chart(fig_pol1, use_container_width=True)

    # Generamos columnas para poder desplegar las tablas cada una con la mitad de la pagina
    col1, col2 = st.columns(2)
    with col1:
        st.table(activities_closed)
    with col2:
        st.table(activities_open)

    # Informa el promedio de tiempo para cerrar una actividad
    st.info(f"Promedio de tiempo de cierre de actividad: {avg_solved['promedio_solucion'].iloc[0]} dias")

    # Se genera la ruta para la grafica de actividades cerradas y abiertas
    img_file1 = f"{semi_path_img}act_{semipath_name}.png"

    # Se genera la ruta para las tablas de actividades abiertas y cerradas
    tab_file1 = f"{semi_path_img}tab1act_{semipath_name}.png"
    tab_file2 = f"{semi_path_img}tab2act_{semipath_name}.png"

    # Genera las graficas y tablas como una imagen en la ruta antes mencionada
    table_act_close.write_image(tab_file1)
    table_act_open.write_image(tab_file2)
    fig_pol1.write_image(img_file1)

    # Agrega tanto las rutas como el titulo de cada grafica.
    image_files.append((img_file1, "Actividades Abiertas y Cerradas"))
    image_files.append((tab_file1, "Tabla Actividades Abiertas"))
    image_files.append((tab_file2, "Tabla Actividades Cerradas"))

# Gráficas: Facturación
# Consulta los costos totales por actividad y por cliente 
state_bill, activities_bill, client_bill = bd.obtener_metricas_facturacion_report(start_date, end_date)
# Comprueba que el resultado no este vació
if state_bill:
    # Calculo de altura precisa para las tablas
    num_filas = len(activities_bill)
    num_filas2 = len(client_bill)

    # Genera la primera grafica de pastel para los costos por actividad
    fig_pie_1 = go.Figure(go.Pie(
        labels='#' + activities_bill['idActividad'].astype(str) + ': ' + activities_bill['nombre_a'], # Se da como label el id y el nombre de la actividad
        values=activities_bill['total'],
        hole=0.4,
        textinfo='value',
        hoverinfo='label+value',
        showlegend=True,
        marker=dict(colors=px.colors.sequential.RdBu)
    ))

    # Actualiza la grafica, dandole un titulo
    fig_pie_1.update_layout(title_text="Costo por Actividad", paper_bgcolor='rgba(0, 0, 0, 0)')
    
    # Genera la segunda grafica de pastel para los costos por cliente
    fig_pie_2 = go.Figure(go.Pie(
        labels='#' + client_bill['idCliente'].astype(str) +': '+client_bill['nombre_c'], # Se da como label el id y el nombre del cliente 
        values=client_bill['total'],
        hole=0.4,
        textinfo='value',
        hoverinfo='label+value',
        showlegend=True,
        marker=dict(colors=px.colors.sequential.RdBu_r)
    ))

    # Actualiza la grafica, dandole un titulo
    fig_pie_2.update_layout(title_text="Costo por Cliente", paper_bgcolor='rgba(0, 0, 0, 0)')
    
    # Se generan columnas para distribuir las graficas en la pagina
    col1, col2 = st.columns(2)

    # Genera una tabla para mostrar los datos de costos por actividad
    table_bill_act = go.Figure(
        go.Table(
            header=dict(
                values=["ID Actividad", "Nombre", "Total"],  # Títulos de las columnas
                font=dict(color='white'),  # Color del texto del encabezado
                fill_color=px.colors.sequential.RdBu[0]  # Usamos el primer color de la paleta para el encabezado
            ),
            cells=dict(
                # Valores de las columnas
                values=[
                    activities_bill[activities_bill.columns[0]],
                    activities_bill[activities_bill.columns[1]], 
                    activities_bill[activities_bill.columns[2]]
                ],
                font=dict(color='white'),  # Color del texto de las celdas
                fill_color=[px.colors.sequential.RdBu[2], px.colors.sequential.RdBu[2]]  # Aplicar dos colores alternados para las columnas
            )
        )
    )

    # Actualiza la tabla para darle la altura precisa
    table_bill_act.update_layout(
        height=ut.det_height_table(num_filas),
        margin=dict(l=0, r=0, t=0, b=0),  # Eliminar los márgenes (izquierda, derecha, arriba y abajo)
        paper_bgcolor='rgba(0,0,0,0)'  # Hacer el fondo transparente
    )

    # Genera una tabla para mostrar los datos de costos por cliente
    table_bill_client = go.Figure(
        go.Table(
            header=dict(
                values=["ID Cliente", "Nombre", "Total"],  # Títulos de las columnas
                font=dict(color='white'),  # Color del texto del encabezado
                fill_color=px.colors.sequential.RdBu[0]  # Usamos el primer color de la paleta para el encabezado
            ),
            cells=dict(
                # Valores de las columnas
                values=[
                    client_bill[client_bill.columns[0]],
                    client_bill[client_bill.columns[1]], 
                    client_bill[client_bill.columns[2]]
                ],
                font=dict(color='white'),  # Color del texto de las celdas
                fill_color=[px.colors.sequential.RdBu[2], px.colors.sequential.RdBu[2]]  # Aplicar dos colores alternados para las columnas
            )
        )
    )

    # Actualiza la tabla para darle la altura precisa
    table_bill_client.update_layout(
        height=ut.det_height_table(num_filas2),
        margin=dict(l=0, r=0, t=0, b=0),  # Eliminar los márgenes (izquierda, derecha, arriba y abajo)
        paper_bgcolor='rgba(0,0,0,0)'  # Hacer el fondo transparente
    )
    
    # Hace la suma de costos para obtener el total
    # Solo se necesita hacer de un dataframe, de los dos seria redundante
    sum_activities_bill = activities_bill['total'].sum()

    # Le damos formato para solo mostrar dos digitos despues del punto
    activities_bill["total"] = activities_bill["total"].apply(lambda x: f"{x:.2f}")
    client_bill["total"] = client_bill["total"].apply(lambda x: f"{x:.2f}")

    # Las graficas y tablas se muestran en dos columnas, ocupando cada uno la mitad de la pagina
    with col1:
        st.plotly_chart(fig_pie_1, use_container_width=True)
        st.table(activities_bill)
    with col2:
        st.plotly_chart(fig_pie_2, use_container_width=True)
        st.table(client_bill)

    # Se presenta el total de costos
    st.info(f"Total de Costos: ${sum_activities_bill} ")

    # Generacion de rutas absolutas con el estandar de nombre para las imagenes y tablas
    img_file2 = f"{semi_path_img}cost_client_{semipath_name}.png"
    img_file3 = f"{semi_path_img}cost_act_{semipath_name}.png"
    tab_file3 = f"{semi_path_img}tab_act_bill{semipath_name}.png"
    tab_file4 = f"{semi_path_img}tab_client_bill{semipath_name}.png"

    # Generación de imagenes de las graficas y tablas
    fig_pie_1.write_image(img_file2)
    fig_pie_2.write_image(img_file3)
    table_bill_act.write_image(tab_file3)
    table_bill_client.write_image(tab_file4)

    # Agrega rutas y titulos en la lista
    image_files.append((img_file2, "Costo por Actividad"))
    image_files.append((img_file3, "Costo por Cliente"))
    image_files.append((tab_file3, "Tabla Costo por Actividad"))
    image_files.append((tab_file4, "Tabla Costo por Cliente"))

# Gráfica: Uso de herramientas y materiales
# Consulta el numero de materiales y herramientas utilizadas en un rango de fechas, divido por fecha
resource_report_material, resource_report_tool, state_report_matool = bd.obtener_recursos_tipo(start_date, end_date)
if state_report_matool:
    # Calculo de altura para las tablas de acuerdo al numero de filas
    num_filas = len(resource_report_material)
    num_filas2 = len(resource_report_tool)

    # Creación de grafica poligonal para los materiales y herramientas
    fig_pol2 = go.Figure()

    # Agrega el trazado del numero de materiales usados por fecha
    fig_pol2.add_trace(go.Scatter(
        x=resource_report_material['fecha'],
        y=resource_report_material['no_materiales'],
        mode='lines+markers',
        name='Material',
        line=dict(color=px.colors.sequential.RdBu[0])
    ))
    
    # Agrega el trazado del numero de herramientas usados por fecha
    fig_pol2.add_trace(go.Scatter(
        x=resource_report_tool['fecha'],
        y=resource_report_tool['no_herramientas'],
        mode='lines+markers',
        name='Herramienta',
        line=dict(color=px.colors.sequential.RdBu_r[0])
    ))

    # Actualizacion de la grafica para incorporar los titulso y eliminar el fondo
    fig_pol2.update_layout(
        title="Uso de Herramientas y Materiales por Día",
        xaxis_title="Fecha",
        yaxis_title="Recursos",
        paper_bgcolor='rgba(0, 0, 0, 0)'
    )

    # Genera la tabla para el numero de herramientas por fecha
    table_tool = go.Figure(
        go.Table(
            header=dict(
                values=["Fecha", "No. Recursos"],  # Títulos de las columnas
                font=dict(color='white'),  # Color del texto del encabezado
                fill_color=px.colors.sequential.RdBu[0]  # Usamos el primer color de la paleta para el encabezado
            ),
            cells=dict(
                values=[
                    resource_report_tool[resource_report_tool.columns[0]],
                    resource_report_tool[resource_report_tool.columns[1]]
                ],
                font=dict(color='white'),  # Color del texto de las celdas
                fill_color=[px.colors.sequential.RdBu[2], px.colors.sequential.RdBu[2]]  # Aplicar dos colores alternados para las columnas
            )
        )
    )
    
    # Actualiza la tabla para modificar la altura de la tabla de acuerdo con el numero de filas
    table_tool.update_layout(
        height=ut.det_height_table(num_filas),
        margin=dict(l=0, r=0, t=0, b=0),  # Eliminar los márgenes (izquierda, derecha, arriba y abajo)
        paper_bgcolor='rgba(0,0,0,0)'  # Hacer el fondo transparente
    )

    # Genera la tabla para el numero de materiales por fecha
    table_material = go.Figure(
        go.Table(
            header=dict(
                values=["Fecha", "No. Recursos"],  # Títulos de las columnas
                font=dict(color='white'),  # Color del texto del encabezado
                fill_color=px.colors.sequential.RdBu[0]  # Usamos el primer color de la paleta para el encabezado
            ),
            cells=dict(
                values=[
                    resource_report_material[resource_report_material.columns[0]],
                    resource_report_material[resource_report_material.columns[1]]
                ],
                font=dict(color='white'),  # Color del texto de las celdas
                fill_color=[px.colors.sequential.RdBu[2], px.colors.sequential.RdBu[2]]  # Aplicar dos colores alternados para las columnas
            )
        )
    )

    # Actualiza la tabla para modificar la altura de la tabla de acuerdo con el numero de filas
    table_material.update_layout(
        height=ut.det_height_table(num_filas),
        margin=dict(l=0, r=0, t=0, b=0),  # Eliminar los márgenes (izquierda, derecha, arriba y abajo)
        paper_bgcolor='rgba(0,0,0,0)'  # Hacer el fondo transparente
    )
    
    # Despliega la grafica donde muestra el numero de herramientas y materiales utilizados por fecha
    st.plotly_chart(fig_pol2, use_container_width=True)
    
    # Genera columnas para darle orden a los graficos, en este caso, cada grafico ocupa la mitad de la pagina
    col1, col2 = st.columns(2)
    with col1: 
        st.table(resource_report_tool)
        # Determina y despliega el promedio de herramientas usadas por dia.
        st.info(f"El promedio de herramientas usadas por día: {resource_report_tool['no_herramientas'].mean()}")
    with col2: 
        st.table(resource_report_material)
        # Determina y despliega el promedio de materiales usados por dia.
        st.info(f"El promedio de materiales usados por día: {resource_report_material['no_materiales'].mean()}")

    # Crea las rutas absolutas para las graficas y tablas
    img_file4 = f"{semi_path_img}tool_material_{semipath_name}.png"
    tab_file5 = f"{semi_path_img}table_tool_{semipath_name}.png"
    tab_file6 = f"{semi_path_img}table_material_{semipath_name}.png"

    # Genera imagenes de las graficas y tablas
    fig_pol2.write_image(img_file4)
    table_tool.write_image(tab_file5)
    table_material.write_image(tab_file6)

    # Agrega las rutas y los titulos de las imagenes en la lista
    image_files.append((img_file4, "Uso de Herramientas y Materiales por Día"))
    image_files.append((tab_file5, "Tabla Herramientas"))
    image_files.append((tab_file6, "Tabla Materiales"))

# Gráfica: Actividades por miembro
# Consulta para obtener las actividades realizadas por cada miembro en el rango de fechas
support_report, state_report = bd.obtener_actividades_miembro(start_date, end_date)
# Verifica que el resultado no sea vacio
if state_report:
    # Calculo de altura para la tabla 
    num_filas = len(support_report)

    # Crea la grafica de barras horizontal para desplegar la cantidad de actividades realizadas por miembro
    fig = go.Figure()
    
    # Añadimos los datos en un trazado
    fig.add_trace(go.Bar(
        x=support_report['actividades'],
        y=support_report['nombre_m'],
        textposition='auto',
        orientation='h',
        name="Promedio de Actividades",
        marker=dict(color=px.colors.sequential.RdBu)
    ))
   
    # Actauliza la grafica para agregar titulos y modificar el ancho de las barras
    fig.update_layout(
        title="Actividades por Miembro",
        xaxis_title="Cantidad de Actividades",
        yaxis_title="Miembro", 
        bargap=0.5,
        bargroupgap=0.3
    )

    # Genera una tabla para mostrar la información de las actividades realizadas por cada miembro
    table_support = go.Figure(
        go.Table(
            header=dict(
                values=["ID Miembro", "Nombre", "No. Actividades"],  # Títulos de las columnas
                font=dict(color='white'),  # Color del texto del encabezado
                fill_color=px.colors.sequential.RdBu[0]  # Usamos el primer color de la paleta para el encabezado
            ),
            cells=dict(
                values=[
                    support_report[support_report.columns[0]],
                    support_report[support_report.columns[1]],
                    support_report[support_report.columns[2]]
                ],
                font=dict(color='white'),  # Color del texto de las celdas
                fill_color=[px.colors.sequential.RdBu[2], px.colors.sequential.RdBu[2]]  # Aplicar dos colores alternados para las columnas
            )
        )
    )

    # Actualiza la tabla para agregar titutlos y eliminar el fondo, tambien cambia el tamaño de la tabla basado en el numero de filas
    table_support.update_layout(
        height=ut.det_height_table(num_filas),
        margin=dict(l=0, r=0, t=0, b=0),  # Eliminar los márgenes (izquierda, derecha, arriba y abajo)
        paper_bgcolor='rgba(0,0,0,0)'  # Hacer el fondo transparente
    )

    # Despliega la grafica y luego la tabla
    st.plotly_chart(fig, use_container_width=True)
    st.table(support_report)

    # Genera las rutas absolutas de para la grafica y la tabla
    img_file5 = f"{semi_path_img}act_supp_{semipath_name}.png"
    tab_file7 = f"{semi_path_img}tab_supp_{semipath_name}.png"

    # Genera las imagenes a partir de la grafica y la tabla
    fig.write_image(img_file5)
    table_support.write_image(tab_file7)

    # Agrega la ruta y el titulo de la imagen a la lista.
    image_files.append((img_file5, "Actividades por Miembro"))
    image_files.append((tab_file7, "Tabla Actividades Por Miembro"))

# Función para generar PDF
def generar_pdf_latex(image_files, promedio_sol, output_file=f"reporte_{semipath_name}.pdf"):
    """
    Genera un PDF apartir de un documento latex y una lista de imagenes.

    Parameters:
    image_files (list): Lista que contiene ruta y titulo de una imagen.
    output_file (str): Ruta con nombre del archivo de salida.

    Returns:
    None: Esa función no regresa ningún valor.
    """

    # Se hace la creación de un documento LaTex
    doc = Document(documentclass="report")
    
    # Seccion de encabezado, se usa la sintaxis de LaTex
    doc.preamble.append(NoEscape(r'\usepackage{graphicx}'))
    doc.preamble.append(NoEscape(r'\usepackage{helvet} '))
    doc.preamble.append(NoEscape(r'\usepackage[margin=1in]{geometry}'))
    doc.preamble.append(NoEscape(r'\renewcommand{\familydefault}{\sfdefault} '))
    doc.preamble.append(NoEscape(r"\title{Reporte de " + range_selected + "}"))
    doc.preamble.append(NoEscape(r"\author{"+st.session_state['name']+r" \\ Appliance Technologies México}"))
    doc.preamble.append(NoEscape(r"\date{\today}"))

    # Se crea el titulo con la directiva de LaTex
    doc.append(NoEscape(r"\maketitle"))

    # Crea una seccion dentro del documento y le da el titulo de la primer imagen
    with doc.create(Section(image_files[0][1])):
        # Escribe dentro del codigo
        doc.append("En el periodo previsto, se analizarón las actividades cerrradas y abiertas por fecha, teniendo como resultado lo siguiente: ")
        
        # Agrega la imagen de actividades cerradas y abiertas al reporte
        with doc.create(Figure(position='h!')) as fig: 
            fig.add_image(image_files[0][0], width=NoEscape(r'0.8\textwidth'))

        # Agrega las tablas de actividades abiertas y cerradas al reporte, utilizando cada una la mitad de la página.
        with doc.create(Figure(position='h!')) as fig:
            fig.append(NoEscape(r"""
            \begin{minipage}{0.48\textwidth} 
                \includegraphics[width=\textwidth]{""" + image_files[1][0] + r"""}
                \centering
                \caption{"""+image_files[1][1] +r"""}
            \end{minipage}
            \hfill
            \begin{minipage}{0.48\textwidth}
                \includegraphics[width=\textwidth]{""" + image_files[2][0] + r"""}
                \centering
                \caption{"""+image_files[2][1] +r"""}
            \end{minipage}
            """))

        # Escribe la anotación de promedio de solución de actividad
        doc.append(NoEscape(r"Durante el périodo observado se noto que el promedio de solución de actividades fue de \textbf{"
        + f"{promedio_sol}"
        + r"} dias"))

    # Hace un salto de una pagina
    doc.append(NoEscape(r"\newpage"))

    #Crea la seccion para los costos en el documento
    with doc.create(Section("Costos")):
        
        # Agrega las graficas para costos por actividad y cliente, respectivamente. Cada una ocupa la mitad de la pagina
        with doc.create(Figure(position='h!')) as fig:
            fig.append(NoEscape(r"""
            \begin{minipage}{0.48\textwidth} 
                \includegraphics[width=\textwidth]{""" + image_files[3][0] + r"""}
                \centering
                \caption{"""+image_files[3][1] +r"""}
            \end{minipage}
            \hfill
            \begin{minipage}{0.48\textwidth}
                \includegraphics[width=\textwidth]{""" + image_files[4][0] + r"""}
                \centering
                \caption{"""+image_files[4][1] +r"""}
            \end{minipage}
            """))
        
        # Agrega las tablas para costos por actividad y cliente, respectivamente. Cada una ocupa la mitad de la pagina
        with doc.create(Figure(position='h!')) as fig:
            fig.append(NoEscape(r"""
            \begin{minipage}{0.48\textwidth} 
                \includegraphics[width=\textwidth]{""" + image_files[5][0] + r"""}
                \centering
                \caption{"""+image_files[5][1] +r"""}
            \end{minipage}
            \hfill
            \begin{minipage}{0.48\textwidth}
                \includegraphics[width=\textwidth]{""" + image_files[6][0] + r"""}
                \centering
                \caption{"""+image_files[6][1] +r"""}
            \end{minipage}
            """))
        
        # Se agrega el total de costos, en forma de texto 
        doc.append(NoEscape(r"Durante el périodo observado el total de costos fue de \textbf{\$"
            + f"{sum_activities_bill}"
            + r"} MXN"))

    # Hace un salto de página   
    doc.append(NoEscape(r"\newpage"))

    # Creamos la sección de inventario
    with doc.create(Section("Inventario")):
        doc.append("En el periodo previsto, el uso de Herramientas y Materiales fue el siguiente: ")
        
        # Agrega la grafica de materiales y herramientas utilizados
        with doc.create(Figure(position='h!')) as fig: 
            fig.add_image(image_files[7][0], width=NoEscape(r'0.8\textwidth'))
        
        # Agrega las tablas de herramientas y materiales, respectivamente 
        with doc.create(Figure(position='h!')) as fig:
            fig.append(NoEscape(r"""
            \begin{minipage}{0.48\textwidth} 
                \includegraphics[width=\textwidth]{""" + image_files[8][0] + r"""}
                \centering
                \caption{"""+image_files[8][1] +r"""}
            \end{minipage}
            \hfill
            \begin{minipage}{0.48\textwidth}
                \includegraphics[width=\textwidth]{""" + image_files[9][0] + r"""}
                \centering
                \caption{"""+image_files[9][1] +r"""}
            \end{minipage}
            """))

        # Se agrega el promedio de herramientas y materiales
        doc.append(NoEscape(r"Se utilizo un promedio de \textbf{" + f"{resource_report_tool['no_herramientas'].mean()}"+ r"} Herramientas y un promedio de \textbf{"+
                            f"{resource_report_material['no_materiales'].mean()}"+
                            r"} Materiales por día."))

    # Realiza un salto de pagina    
    doc.append(NoEscape(r"\newpage"))
    
    # Crea una seccion para los miembros
    with doc.create(Section("Miembros")):
        doc.append("En el periodo previsto, la productividad de los Miembros fue: ")
        
        # Agrega la grafica de barras para la cantidad de actividades por mimebro
        with doc.create(Figure(position='h!')) as fig: 
            fig.add_image(image_files[10][0], width=NoEscape(r'0.8\textwidth'))
        
        # Agrega la tabla para la cantidad de actividades por miembro 
        with doc.create(Figure(position='h!')) as fig: 
            fig.add_image(image_files[11][0], width=NoEscape(r'0.8\textwidth'))
            fig.add_caption(image_files[11][1])

    # Se agrega el periodo en el que fueron recuperados los datos
    doc.append(NoEscape(r"\textit{Datos obtenidos para el periodo " + f"{start_date}" + r" al " + f"{end_date}" + r"}"))
    
    # La funcion genera el documento PDF
    doc.generate_pdf(output_file.split('.')[0], clean_tex=True)

with st.container(): 
    # Renderiza y captura la accion del botón que genera el PDF
    if st.button("Generar PDF", use_container_width=True):
        output_pdf = f"reporte_{semipath_name}.pdf"
        
        # Se genera un if para que no muestre información que no puede ser calculada en caso de no tener datos
        if avg_solved.empty: 
            promedio_sol = 0.0
        else:
            promedio_sol = avg_solved['promedio_solucion'].iloc[0]
        
        # Manda a llamar la función de generacion de LaTex
        generar_pdf_latex(image_files,promedio_sol, "reports/"+output_pdf)
        st.success(f"PDF generado exitosamente: {output_pdf}")
        
        # Se accede al documento usando la ruta. 
        with open("reports/"+output_pdf, "rb") as pdf_file:
            # Permite descargar el pdf del documento del reporte que generamos
            st.download_button("Descargar PDF", data=pdf_file, file_name=f"reporte_{semipath_name}.pdf", mime="application/pdf")
