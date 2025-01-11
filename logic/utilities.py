from datetime import datetime
from dateutil.relativedelta import relativedelta

def get_today_date():
    """
    Obtiene la fecha actual en formato 'YYYY-MM-DD'.

    Returns:
        str: Fecha actual en formato 'YYYY-MM-DD'.
    """
    datetoday = datetime.now()
    dates_ins_resource = datetoday.strftime("%Y-%m-%d")
    return dates_ins_resource

def get_total_days_life(vida_util, fecha_ingreso):
    """
    Calcula el número total de días de vida útil y los días transcurridos desde la fecha de ingreso.

    Args:
        vida_util (str): Vida útil del recurso ('10 Años', '5 Años', '1 Año').
        fecha_ingreso (datetime.date): Fecha de ingreso del recurso.

    Returns:
        tuple: Días transcurridos desde la fecha de ingreso, y días totales de vida útil.
    """
    if vida_util == "10 Años":
        dias_totales = 3650
    elif vida_util == "5 Años":
        dias_totales = 1825
    elif vida_util == "1 Año":
        dias_totales = 365
    dias_vida = (datetime.now().date() - fecha_ingreso).days

    return dias_vida, dias_totales

def dict_resource_upd(resource_data_type, resource_data_life, resource_data_status):
    """
    Convierte las características de un recurso en índices numéricos.

    Args:
        resource_data_type (str): Tipo de recurso ('Herramienta', 'Material').
        resource_data_life (str): Vida útil del recurso ('1 Vez', '1 Año', '5 Años', '10 Años').
        resource_data_status (str): Estado del recurso ('En Stock', 'En Uso').

    Returns:
        tuple: Índices numéricos correspondientes al tipo, vida útil y estado del recurso.
    """
    type_dict = {
        "Herramienta": 0,
        "Material": 1
    }

    life_dict = {
        "1 Vez": 0,
        "1 Año": 1,
        "5 Años": 2,
        "10 Años": 3 
    }

    status_dict = {
        "En Stock": 0,
        "En Uso": 1
    }

    index_type = type_dict[resource_data_type]
    index_life = life_dict[resource_data_life]
    index_status = status_dict[resource_data_status]

    return index_type, index_life, index_status

def dict_support_upd(support_data):
    """
    Convierte el estado de soporte en un índice numérico.

    Args:
        support_data (str): Estado de soporte ('Libre', 'Vacaciones', 'En Actividad', 'Incapacidad').

    Returns:
        int: Índice numérico correspondiente al estado de soporte.
    """
    status_dict = {
            "Libre": 0,
            "Vacaciones": 1,
            "En Actividad": 2,
            "Incapacidad": 3
        }

    index_status = status_dict[support_data]

    return index_status

def dict_activity_upd(type, status):
    """
    Convierte el tipo y estado de una actividad en índices numéricos.

    Args:
        type (str): Tipo de actividad ('Matenimiento', 'Incidencia').
        status (str): Estado de la actividad ('Abierto', 'En Curso', 'Pendiente').

    Returns:
        tuple: Índices numéricos correspondientes al tipo y estado de la actividad.
    """
    type_dict = {
        "Matenimiento": 0,
        "Incidencia": 1
    }

    status_dict = {
        "Abierto": 0,
        "En Curso": 1,
        "Pendiente": 2,
    }

    index_type = type_dict[type]
    index_status = status_dict[status]
        
    return index_type, index_status

def dict_bill_upd(type, status):
    """
    Convierte el tipo y estado de una factura en índices numéricos.

    Args:
        type (str): Tipo de factura ('Viaje', 'Comida', 'Hospedaje').
        status (str): Estado de la factura ('Abierta', 'Pendiente').

    Returns:
        tuple: Índices numéricos correspondientes al tipo y estado de la factura.
    """
    type_dict = {
                "Viaje": 0,
                "Comida": 1,
                "Hospedaje": 2
            }

    status_dict = {
        "Abierta": 0,
        "Pendiente": 1
    }

    index_type = type_dict[type]
    index_status = status_dict[status]

    return index_type, index_status

def date_report(range_selected):
    """
    Calcula las fechas de inicio y fin para un rango de tiempo seleccionado.

    Args:
        range_selected (str): Rango de tiempo ('1 Semana', '1 Mes', '6 Meses').

    Returns:
        tuple: Fechas de fin e inicio en formato 'YYYY-MM-DD'.
    """
    end_date = datetime.now()

    if range_selected == "1 Semana":
        start_date = end_date - relativedelta(weeks=1)
    elif range_selected == "1 Mes":
        start_date = end_date - relativedelta(months=1)
    elif range_selected == "6 Meses":
        start_date = end_date - relativedelta(months=6)
    else:
        start_date = None

    return end_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d')

def det_height_table(num_filas):
    """
    Determina la altura de una tabla en función del número de filas.

    Args:
        num_filas (int): Número de filas en la tabla.

    Returns:
        int: Altura de la tabla.
    """
    fig_height = 30 + (20 * num_filas)
    return fig_height