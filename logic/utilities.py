from datetime import datetime
from dateutil.relativedelta import relativedelta

def get_today_date():
    datetoday = datetime.now()
    dates_ins_resource = datetoday.strftime("%Y-%m-%d")
    return dates_ins_resource

def get_total_days_life(vida_util, fecha_ingreso):
    if vida_util == "10 Años":
        dias_totales = 3650
    elif vida_util == "5 Años":
        dias_totales = 1825
    elif vida_util == "1 Año":
        dias_totales = 365    
    dias_vida = (datetime.now().date() - fecha_ingreso).days

    return dias_vida, dias_totales

def dict_resource_upd(resource_data_type, resource_data_life, resource_data_status):
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
    status_dict = {
            "Libre": 0,
            "Vacaciones": 1,
            "En Actividad": 2,
            "Incapacidad": 3
        }

    index_status = status_dict[support_data]

    return index_status

def dict_activity_upd(type, status):
    # Necesitamos ademas saber el index del tipo, vida_util, estado
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
    fig_height = 30 + (20 * num_filas)
    return fig_height