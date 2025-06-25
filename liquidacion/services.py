from decimal import Decimal
from liquidacion.models import Liquidacion, ConceptoLiquidacion, Concepto, ConcEmpLiquidacion
from empleado.models import Empleado
from contrato.models import Contrato
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

    liquidaciones = Liquidacion.objects.filter(mes_liquidacion=mes, anho_liquidacion=anho) if mes and anho else Liquidacion.objects.all()
    conceptos_qs = ConceptoLiquidacion.objects.filter(id_empleado=empleado)
    conceptos_ids = conceptos_qs.values_list('id_concepto_liquidacion', flat=True)

    liquidacion_ids = ConcEmpLiquidacion.objects.filter(
        id_concepto_liquidacion__in=conceptos_ids,
        id_liquidacion__in=liquidaciones
    ).values_list('id_liquidacion', flat=True)

    liquidacion = Liquidacion.objects.filter(id_liquidacion__in=liquidacion_ids).order_by('-fecha_liquidacion').first()

    conceptos_liq = []
    if liquidacion:
        conceptos_liq_ids = ConcEmpLiquidacion.objects.filter(
            id_liquidacion=liquidacion
        ).values_list('id_concepto_liquidacion', flat=True)

        conceptos_liq = ConceptoLiquidacion.objects.filter(
            id_concepto_liquidacion__in=conceptos_liq_ids
        ).select_related('id_concepto')

    bonificaciones = Decimal('0')
    descuentos = Decimal('0')
    nombres_conceptos_cargados = set()

    for c in conceptos_liq:
        concepto = c.id_concepto
        if not concepto:
            continue

        nombres_conceptos_cargados.add(concepto.descripcion.lower())

        if concepto.es_deb_cred:
            bonificaciones += c.monto
        else:
            descuentos += c.monto

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
