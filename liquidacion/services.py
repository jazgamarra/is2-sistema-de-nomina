from decimal import Decimal
from liquidacion.models import Liquidacion, ConceptoLiquidacion, Concepto, ConcEmpLiquidacion
from empleado.models import Empleado
from contrato.models import Contrato
from .models import DebCredMes  # asegurate de tener el import

from datetime import date   

def calcular_sueldo_detallado(id_empleado, mes=None, anho=None):
    empleado = Empleado.objects.get(pk=id_empleado)

    contrato = Contrato.objects.filter(id_empleado=empleado, contrato_activo=True).order_by('-fecha_inicio').first()
    if not contrato:
        return {
            'salario_base': Decimal('0'),
            'bonificaciones': Decimal('0'),
            'descuentos': Decimal('0'),
            'sueldo_total': Decimal('0')
        }

    salario_base = contrato.salario_acordado or contrato.salario

    conceptos_liq = []
    nombres_conceptos_cargados = set()

    # Intentar obtener la liquidación del mes/año
    if mes and anho:
        liquidacion = Liquidacion.objects.filter(mes_liquidacion=mes, anho_liquidacion=anho).order_by('-fecha_liquidacion').first()
    else:
        liquidacion = Liquidacion.objects.filter().order_by('-fecha_liquidacion').first()

    if liquidacion:
        conceptos_liq_ids = ConcEmpLiquidacion.objects.filter(
            id_liquidacion=liquidacion
        ).values_list('id_concepto_liquidacion', flat=True)

        conceptos_liq = ConceptoLiquidacion.objects.filter(
            id_concepto_liquidacion__in=conceptos_liq_ids,
            id_empleado=empleado
        ).select_related('id_concepto')
    else:
        # 🔁 Si aún no hay liquidación, usamos los conceptos desde DebCredMes
        conceptos_liq = DebCredMes.objects.filter(
            id_empleado=empleado.id_empleado,
            mes=mes,
            anho=anho
        ).select_related('id_concepto')

    bonificaciones = Decimal('0')
    descuentos = Decimal('0')

    for c in conceptos_liq:
        concepto = c.id_concepto
        if not concepto:
            continue

        nombres_conceptos_cargados.add(concepto.descripcion.lower())

        if concepto.es_deb_cred:
            bonificaciones += c.monto  # ✅ crédito = bonificación
        else:
            descuentos += c.monto      # ✅ débito = descuento

    # BONO POR HIJOS (solo si no está cargado)
    if 'bonificacion_por_hijos' not in nombres_conceptos_cargados and empleado.hijos_menores_18 > 0:
        concepto_hijos = Concepto.objects.filter(descripcion__iexact='bonificacion_por_hijos').first()
        if concepto_hijos:
            porcentaje = Decimal(concepto_hijos.porcentaje or 0)
            bonificaciones += (salario_base * porcentaje / 100) * empleado.hijos_menores_18

    # DESCUENTO IPS
    if 'descuento_ips' not in nombres_conceptos_cargados and empleado.aplica_ips:
        concepto_ips = Concepto.objects.filter(descripcion__iexact='descuento_ips').first()
        if concepto_ips:
            porcentaje = Decimal(concepto_ips.porcentaje or 0)
            descuentos += salario_base * porcentaje / 100

    # BONOS AUTOMÁTICOS COMUNES
    for bono in ['bono_por_productividad', 'premio_asistencia']:
        if bono not in nombres_conceptos_cargados:
            concepto_bono = Concepto.objects.filter(descripcion__iexact=bono).first()
            if concepto_bono:
                porcentaje = Decimal(concepto_bono.porcentaje or 0)
                bonificaciones += salario_base * porcentaje / 100

    sueldo_total = salario_base + bonificaciones - descuentos

    return {
        'salario_base': salario_base,
        'bonificaciones': bonificaciones,
        'descuentos': descuentos,
        'sueldo_total': sueldo_total
    }


def generar_datos_nomina_todos():
    empleados = Empleado.objects.all()
    nominas = []

    for emp in empleados:
        datos = calcular_sueldo_detallado(emp.id_empleado)
        nominas.append({
            'empleado': emp,
            'salario': datos['salario_base'],
            'bonos': datos['bonificaciones'],
            'descuentos': datos['descuentos'],
            'total': datos['sueldo_total'],
        })

    return nominas

