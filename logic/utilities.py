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
