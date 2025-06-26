from django.shortcuts import render
from django.db.models import Sum
from datetime import date

from liquidacion.models import Liquidacion, ConceptoLiquidacion, Concepto, DebCredMes
from empleado.models import Empleado
from liquidacion.models import ConcEmpLiquidacion

def menu_reportes(request):
    return render(request, 'reporte/menu_reportes.html')

def dashboard_general(request):
    hoy = date.today()
    mes = int(request.GET.get('mes', hoy.month))
    anho = int(request.GET.get('anho', hoy.year))

    # Liquidaciones del mes y año actual
    liquidaciones = Liquidacion.objects.filter(
        mes_liquidacion=mes,
        anho_liquidacion=anho
    )

    # Conceptos por empleado en esas liquidaciones
    conceptos_empleados = ConcEmpLiquidacion.objects.filter(
        id_liquidacion__in=liquidaciones
    ).select_related(
        'id_concepto_liquidacion__id_empleado',
        'id_concepto_liquidacion__id_concepto'
    )

    # Agrupamos por empleado
    costos_por_empleado = {}
    for ce in conceptos_empleados:
        cl = ce.id_concepto_liquidacion
        empleado = cl.id_empleado
        concepto = cl.id_concepto
        monto = cl.monto

        if concepto is None:
            continue  # Ignorar conceptos sin referencia válida

        if empleado.id_empleado not in costos_por_empleado:
            costos_por_empleado[empleado.id_empleado] = {
                'empleado': f"{empleado.nombres} {empleado.apellidos}",
                'ingresos': 0,
                'descuentos': 0,
                'total': 0
            }

        if concepto.es_deb_cred:  # descuento
            costos_por_empleado[empleado.id_empleado]['descuentos'] += float(monto)
        else:  # ingreso
            costos_por_empleado[empleado.id_empleado]['ingresos'] += float(monto)

    # Total neto por empleado
    for item in costos_por_empleado.values():
        item['total'] = item['ingresos'] - item['descuentos']

    # Datos para gráfico: distribución de conceptos
    distribucion_conceptos = list(
        DebCredMes.objects
        .filter(mes=mes, anho=anho)
        .values('id_concepto__descripcion')
        .annotate(total=Sum('monto'))
        .order_by('-total')
    )

    # Datos para gráfico: acumulado por empleado
    acumulado_empleados = list(
        DebCredMes.objects
        .filter(mes=mes, anho=anho)
        .values('id_empleado')
        .annotate(total=Sum('monto'))
        .order_by('-total')
    )

    # Mapeamos nombres
    empleados_map = {
        e.id_empleado: f"{e.nombres} {e.apellidos}"
        for e in Empleado.objects.all()
    }

    for e in acumulado_empleados:
        e['nombre'] = empleados_map.get(e['id_empleado'], 'Desconocido')

    context = {
        'mes': mes,
        'anho': anho,
        'costos_por_empleado': list(costos_por_empleado.values()),
        'distribucion_conceptos': distribucion_conceptos,
        'acumulado_empleados': acumulado_empleados,
    }

    return render(request, 'reporte/dashboard_general.html', context)

def reporte_conceptos(request):
    from datetime import date
    hoy = date.today()
    mes = int(request.GET.get('mes', hoy.month))
    anho = int(request.GET.get('anho', hoy.year))

    distribucion_conceptos = (
        DebCredMes.objects
        .filter(mes=mes, anho=anho)
        .values('id_concepto__descripcion')
        .annotate(total=Sum('monto'))
        .order_by('-total')
    )

    return render(request, 'reporte/reporte_conceptos.html', {
        'mes': mes,
        'anho': anho,
        'distribucion_conceptos': list(distribucion_conceptos)
    })

def reporte_costo_empleado(request):
    hoy = date.today()
    mes = int(request.GET.get('mes', hoy.month))
    anho = int(request.GET.get('anho', hoy.year))

    acumulado_empleados = (
        DebCredMes.objects
        .filter(mes=mes, anho=anho)
        .values('id_empleado')
        .annotate(total=Sum('monto'))
        .order_by('-total')
    )

    empleados_map = {
        e.id_empleado: f"{e.nombres} {e.apellidos}"
        for e in Empleado.objects.all()
    }

    for e in acumulado_empleados:
        e['nombre'] = empleados_map.get(e['id_empleado'], 'Desconocido')

    return render(request, 'reporte/reporte_costos_empleados.html', {
        'mes': mes,
        'anho': anho,
        'acumulado_empleados': list(acumulado_empleados)
    })