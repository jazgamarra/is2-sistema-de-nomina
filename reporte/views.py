from django.shortcuts import render
from django.db.models import Sum
from liquidacion.models import ConceptoLiquidacion, Liquidacion, Empleado

def menu_reportes(request):
    return render(request, 'reporte/menu_reportes.html')

def reporte_sueldos(request):
    # Esto se implementará más adelante
    return render(request, 'reporte/reporte_sueldos.html')

def reporte_conceptos(request):
    # Esto se implementará más adelante
    return render(request, 'reporte/reporte_conceptos.html')

def reporte_costos_empleados(request):
    # Esto se implementará más adelante
    return render(request, 'reporte/reporte_costos_empleados.html')


def dashboard_costos_mensuales(request):
    liquidaciones = (
        ConceptoLiquidacion.objects
        .filter(id_concepto__es_deb_cred=False)  # solo débitos
        .select_related('id_liquidacion__id_empleado')
        .values('id_liquidacion__anho_liquidacion', 'id_liquidacion__mes_liquidacion', 'id_liquidacion__id_empleado__nombres', 'id_liquidacion__id_empleado__apellidos')
        .annotate(total=Sum('monto_concepto'))
        .order_by('id_liquidacion__anho_liquidacion', 'id_liquidacion__mes_liquidacion')
    )

    data = {}
    for entry in liquidaciones:
        mes_num = entry['id_liquidacion__mes_liquidacion']
        anho = entry['id_liquidacion__anho_liquidacion']
        if mes_num is None or anho is None:
            continue  # saltar entradas inválidas

        mes = f"{int(mes_num):02d}/{anho}"
        nombre_empleado = (
            f"{entry['id_liquidacion__id_empleado__nombres']} "
            f"{entry['id_liquidacion__id_empleado__apellidos']}"
        )
        monto = entry['total'] or 0  # prevenir None

        if mes not in data:
            data[mes] = {'empleados': [], 'total_mes': 0}

        data[mes]['empleados'].append({
            'nombre': nombre_empleado,
            'monto': monto
        })
        data[mes]['total_mes'] += monto
    
    return render(request, 'reporte/dashboard_costos_mensuales.html', {'data': data})
