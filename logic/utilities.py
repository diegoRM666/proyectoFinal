from datetime import datetime


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