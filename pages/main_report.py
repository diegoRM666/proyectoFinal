import streamlit as st
import pandas as pd
import logic.bd as bd
import logic.utilities as ut
from menu import menu_with_redirect
import plotly.graph_objects as go
import plotly.express as px
from pylatex import Document, Section, Figure, NoEscape, Subsection
import os

# Lógica de menú
menu_with_redirect()

# Título de la aplicación
st.markdown("# 📊 Generación de Reportes")

# Selección del rango de tiempo
col1, col2 = st.columns([8, 2])
with col2:
    range_selected = st.selectbox("Rango", ["1 Semana", "1 Mes", "6 Meses"])

# Obtener rango de fechas
end_date, start_date = ut.date_report(range_selected) 
semipath_name = f"{start_date}_to_{end_date}"
semi_path_img = f"reports/img/"


# Lista para almacenar imágenes de gráficas y sus títulos
image_files = []

# Gráfica: Actividades cerradas y abiertas
activities_closed, activities_open, avg_solved = bd.consultar_actividades_report(start_date, end_date)
if activities_closed is not None and not activities_closed.empty and activities_open is not None and not activities_open.empty:
    # Calculo de altura
    num_filas = len(activities_closed)
    num_filas2 = len(activities_open)

    st.markdown("## Actividades Cerradas y Abiertas")
    fig_pol1 = go.Figure()
    fig_pol1.add_trace(go.Scatter(
        x=activities_closed['fecha_cierre'],
        y=activities_closed['actividades_cerradas'],
        mode='lines+markers',
        name='Cerradas',
        line=dict(color=px.colors.sequential.RdBu[0])
    ))
    fig_pol1.add_trace(go.Scatter(
        x=activities_open['fecha_apertura'],
        y=activities_open['actividades_abiertas'],
        mode='lines+markers',
        name='Abiertas',
        line=dict(color=px.colors.sequential.RdBu_r[0])
    ))
    fig_pol1.update_layout(
        xaxis_title="Fecha",
        yaxis_title="Actividades",
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)'
    )

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

    table_act_close.update_layout(
        height=ut.det_height_table(num_filas),
        margin=dict(l=0, r=0, t=0, b=0),  # Eliminar los márgenes (izquierda, derecha, arriba y abajo)
        paper_bgcolor='rgba(0,0,0,0)'  # Hacer el fondo transparente
    )
    
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

    table_act_open.update_layout(
        height=ut.det_height_table(num_filas2),
        margin=dict(l=0, r=0, t=0, b=0),  # Eliminar los márgenes (izquierda, derecha, arriba y abajo)
        paper_bgcolor='rgba(0,0,0,0)'  # Hacer el fondo transparente
    )


    st.plotly_chart(fig_pol1, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.table(activities_closed)
    with col2:
        st.table(activities_open)

    st.info(f"Promedio de tiempo de cierre de actividad: {avg_solved['promedio_solucion'].iloc[0]} dias")

    img_file1 = f"{semi_path_img}act_{semipath_name}.png"

    tab_file1 = f"{semi_path_img}tab1act_{semipath_name}.png"
    tab_file2 = f"{semi_path_img}tab2act_{semipath_name}.png"

    table_act_close.write_image(tab_file1)
    table_act_open.write_image(tab_file2)

    fig_pol1.write_image(img_file1)

    image_files.append((img_file1, "Actividades Abiertas y Cerradas"))
    image_files.append((tab_file1, "Tabla Actividades Abiertas"))
    image_files.append((tab_file2, "Tabla Actividades Cerradas"))


# Gráficas: Facturación
state_bill, activities_bill, client_bill = bd.obtener_metricas_facturacion_report(start_date, end_date)
if state_bill:
    # Calculo de altura
    num_filas = len(activities_bill)
    num_filas2 = len(client_bill)

    fig_pie_1 = go.Figure(go.Pie(
        labels='#' + activities_bill['idActividad'].astype(str) + ': ' + activities_bill['nombre_a'],
        values=activities_bill['total'],
        hole=0.4,
        textinfo='value',
        hoverinfo='label+value',
        showlegend=True,
        marker=dict(colors=px.colors.sequential.RdBu)
    ))

    fig_pie_1.update_layout(title_text="Costo por Actividad", paper_bgcolor='rgba(0, 0, 0, 0)')
    
    fig_pie_2 = go.Figure(go.Pie(
        labels='#' + client_bill['idCliente'].astype(str) +': '+client_bill['nombre_c'],
        values=client_bill['total'],
        hole=0.4,
        textinfo='value',
        hoverinfo='label+value',
        showlegend=True,
        marker=dict(colors=px.colors.sequential.RdBu_r)
    ))

    fig_pie_2.update_layout(title_text="Costo por Cliente", paper_bgcolor='rgba(0, 0, 0, 0)')
    col1, col2 = st.columns(2)


    table_bill_act = go.Figure(
        go.Table(
            header=dict(
                values=["ID Actividad", "Nombre", "Total"],  # Títulos de las columnas
                font=dict(color='white'),  # Color del texto del encabezado
                fill_color=px.colors.sequential.RdBu[0]  # Usamos el primer color de la paleta para el encabezado
            ),
            cells=dict(
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

    table_bill_act.update_layout(
        height=ut.det_height_table(num_filas),
        margin=dict(l=0, r=0, t=0, b=0),  # Eliminar los márgenes (izquierda, derecha, arriba y abajo)
        paper_bgcolor='rgba(0,0,0,0)'  # Hacer el fondo transparente
    )

    table_bill_client = go.Figure(
        go.Table(
            header=dict(
                values=["ID Cliente", "Nombre", "Total"],  # Títulos de las columnas
                font=dict(color='white'),  # Color del texto del encabezado
                fill_color=px.colors.sequential.RdBu[0]  # Usamos el primer color de la paleta para el encabezado
            ),
            cells=dict(
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

    table_bill_client.update_layout(
        height=ut.det_height_table(num_filas2),
        margin=dict(l=0, r=0, t=0, b=0),  # Eliminar los márgenes (izquierda, derecha, arriba y abajo)
        paper_bgcolor='rgba(0,0,0,0)'  # Hacer el fondo transparente
    )
    
    sum_activities_bill = activities_bill['total'].sum()
    activities_bill["total"] = activities_bill["total"].apply(lambda x: f"{x:.2f}")
    client_bill["total"] = client_bill["total"].apply(lambda x: f"{x:.2f}")

    with col1:
        st.plotly_chart(fig_pie_1, use_container_width=True)
        st.table(activities_bill)
    with col2:
        st.plotly_chart(fig_pie_2, use_container_width=True)
        st.table(client_bill)
    st.info(f"Total de Costos: ${sum_activities_bill} ")

    
    img_file2 = f"{semi_path_img}cost_client_{semipath_name}.png"
    img_file3 = f"{semi_path_img}cost_act_{semipath_name}.png"
    tab_file3 = f"{semi_path_img}tab_act_bill{semipath_name}.png"
    tab_file4 = f"{semi_path_img}tab_client_bill{semipath_name}.png"

    fig_pie_1.write_image(img_file2)
    fig_pie_2.write_image(img_file3)
    table_bill_act.write_image(tab_file3)
    table_bill_client.write_image(tab_file4)

    image_files.append((img_file2, "Costo por Actividad"))
    image_files.append((img_file3, "Costo por Cliente"))
    image_files.append((tab_file3, "Tabla Costo por Actividad"))
    image_files.append((tab_file4, "Tabla Costo por Cliente"))

# Gráfica: Uso de herramientas y materiales
resource_report_material, resource_report_tool, state_report_matool = bd.obtener_recursos_tipo(start_date, end_date)
if state_report_matool:
    # Calculo de altura
    num_filas = len(resource_report_material)
    num_filas2 = len(resource_report_tool)

    fig_pol2 = go.Figure()
    fig_pol2.add_trace(go.Scatter(
        x=resource_report_material['fecha'],
        y=resource_report_material['no_materiales'],
        mode='lines+markers',
        name='Material',
        line=dict(color=px.colors.sequential.RdBu[0])
    ))
    fig_pol2.add_trace(go.Scatter(
        x=resource_report_tool['fecha'],
        y=resource_report_tool['no_herramientas'],
        mode='lines+markers',
        name='Herramienta',
        line=dict(color=px.colors.sequential.RdBu_r[0])
    ))
    fig_pol2.update_layout(
        title="Uso de Herramientas y Materiales por Día",
        xaxis_title="Fecha",
        yaxis_title="Recursos",
        paper_bgcolor='rgba(0, 0, 0, 0)'
    )


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
    
    table_tool.update_layout(
        height=ut.det_height_table(num_filas),
        margin=dict(l=0, r=0, t=0, b=0),  # Eliminar los márgenes (izquierda, derecha, arriba y abajo)
        paper_bgcolor='rgba(0,0,0,0)'  # Hacer el fondo transparente
    )

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

    table_material.update_layout(
        height=ut.det_height_table(num_filas),
        margin=dict(l=0, r=0, t=0, b=0),  # Eliminar los márgenes (izquierda, derecha, arriba y abajo)
        paper_bgcolor='rgba(0,0,0,0)'  # Hacer el fondo transparente
    )
    

    st.plotly_chart(fig_pol2, use_container_width=True)
    col1, col2 = st.columns(2)
    with col1: 
        st.table(resource_report_tool)
        st.info(f"El promedio de herramientas usadas por día: {resource_report_tool['no_herramientas'].mean()}")
    with col2: 
        st.table(resource_report_material)
        st.info(f"El promedio de materiales usados por día: {resource_report_material['no_materiales'].mean()}")


    img_file4 = f"{semi_path_img}tool_material_{semipath_name}.png"
    tab_file5 = f"{semi_path_img}table_tool_{semipath_name}.png"
    tab_file6 = f"{semi_path_img}table_material_{semipath_name}.png"

    fig_pol2.write_image(img_file4)
    table_tool.write_image(tab_file5)
    table_material.write_image(tab_file6)

    image_files.append((img_file4, "Uso de Herramientas y Materiales por Día"))
    image_files.append((tab_file5, "Tabla Herramientas"))
    image_files.append((tab_file6, "Tabla Materiales"))

# Gráfica: Actividades por miembro
support_report, state_report = bd.obtener_actividades_miembro(start_date, end_date)
if state_report:
    # Calculo de altura
    num_filas = len(support_report)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=support_report['actividades'],
        y=support_report['nombre_m'],
        textposition='auto',
        orientation='h',
        name="Promedio de Actividades",
        marker=dict(color=px.colors.sequential.RdBu)
    ))
    fig.update_layout(
        title="Actividades por Miembro",
        xaxis_title="Cantidad de Actividades",
        yaxis_title="Miembro", 
        bargap=0.5,
        bargroupgap=0.3
    )


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

    table_support.update_layout(
        height=ut.det_height_table(num_filas),
        margin=dict(l=0, r=0, t=0, b=0),  # Eliminar los márgenes (izquierda, derecha, arriba y abajo)
        paper_bgcolor='rgba(0,0,0,0)'  # Hacer el fondo transparente
    )

    st.plotly_chart(fig, use_container_width=True)
    st.table(support_report)

    img_file5 = f"{semi_path_img}act_supp_{semipath_name}.png"
    tab_file7 = f"{semi_path_img}tab_supp_{semipath_name}.png"

    fig.write_image(img_file5)
    table_support.write_image(tab_file7)

    image_files.append((img_file5, "Actividades por Miembro"))
    image_files.append((tab_file7, "Tabla Actividades Por Miembro"))

# Función para generar PDF
def generar_pdf_latex(image_files, output_file=f"reporte_{semipath_name}.pdf"):
    doc = Document(documentclass="report")
    doc.preamble.append(NoEscape(r'\usepackage{graphicx}'))
    doc.preamble.append(NoEscape(r'\usepackage{helvet} '))
    doc.preamble.append(NoEscape(r'\usepackage[margin=1in]{geometry}'))
    doc.preamble.append(NoEscape(r'\renewcommand{\familydefault}{\sfdefault} '))
     
    doc.preamble.append(NoEscape(r"\title{Reporte de " + range_selected + "}"))
    doc.preamble.append(NoEscape(r"\author{"+st.session_state['name']+r" \\ Appliance Technologies México}"))
    doc.preamble.append(NoEscape(r"\date{\today}"))

    doc.append(NoEscape(r"\maketitle"))
    #doc.append(f"Datos del {start_date} al {end_date}")
    with doc.create(Section(image_files[0][1])):
        doc.append("En el periodo previsto, se analizarón las actividades cerrradas y abiertas por fecha, teniendo como resultado lo siguiente: ")
        with doc.create(Figure(position='h!')) as fig: 
            fig.add_image(image_files[0][0], width=NoEscape(r'0.8\textwidth'))

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
        doc.append(NoEscape(r"Durante el périodo observado se noto que el promedio de solución de actividades fue de \textbf{"
        + f"{avg_solved['promedio_solucion'].iloc[0]:.2f}"
        + r"} dias"))

    doc.append(NoEscape(r"\newpage"))
    with doc.create(Section("Costos")):
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
        doc.append(NoEscape(r"Durante el périodo observado el total de costos fue de \textbf{\$"
            + f"{sum_activities_bill}"
            + r"} MXN"))
        
    doc.append(NoEscape(r"\newpage"))
    with doc.create(Section("Inventario")):
        doc.append("En el periodo previsto, el uso de Herramientas y Materiales fue el siguiente: ")
        with doc.create(Figure(position='h!')) as fig: 
            fig.add_image(image_files[7][0], width=NoEscape(r'0.8\textwidth'))
        
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

        doc.append(NoEscape(r"Se utilizo un promedio de \textbf{" + f"{resource_report_tool['no_herramientas'].mean()}"+ r"} Herramientas y un promedio de \textbf{"+
                            f"{resource_report_material['no_materiales'].mean()}"+
                            r"} Materiales por día."))
        
    doc.append(NoEscape(r"\newpage"))
    with doc.create(Section("Miembros")):
        doc.append("En el periodo previsto, la productividad de los Miembros fue: ")
        with doc.create(Figure(position='h!')) as fig: 
            fig.add_image(image_files[10][0], width=NoEscape(r'0.8\textwidth'))
        with doc.create(Figure(position='h!')) as fig: 
            fig.add_image(image_files[11][0], width=NoEscape(r'0.8\textwidth'))
            fig.add_caption(image_files[11][1])

    doc.generate_pdf(output_file.split('.')[0], clean_tex=True)

# Botón para generar PDF
with st.container(): 
    if st.button("Generar PDF", use_container_width=True):
        output_pdf = f"reporte_{semipath_name}.pdf"
        generar_pdf_latex(image_files, output_pdf)
        st.success(f"PDF generado exitosamente: {output_pdf}")
        with open(output_pdf, "rb") as pdf_file:
            st.download_button("Descargar PDF", data=pdf_file, file_name=f"reporte_{semipath_name}.pdf", mime="application/pdf")
