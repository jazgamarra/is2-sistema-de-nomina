from decimal import Decimal
from liquidacion.models import Liquidacion, ConceptoLiquidacion, Concepto
from empleado.models import Empleado
from contrato.models import Contrato

def calcular_sueldo_detallado(id_empleado):
    empleado = Empleado.objects.get(pk=id_empleado)

    # ✅ Buscar contrato activo del empleado
    contrato = Contrato.objects.filter(id_empleado=empleado, contrato_activo=True).order_by('-fecha_inicio').first()

    if not contrato:
        return {
            'salario_base': Decimal('0'),
            'bonificaciones': Decimal('0'),
            'descuentos': Decimal('0'),
            'sueldo_total': Decimal('0')
        }

    salario_base = contrato.salario_acordado or contrato.salario  # Usa salario acordado si existe

    # Buscar la última liquidación
    liquidacion = Liquidacion.objects.filter(id_empleado=empleado).order_by('-id_liquidacion').first()

    if not liquidacion:
        return {
            'salario_base': salario_base,
            'bonificaciones': Decimal('0'),
            'descuentos': Decimal('0'),
            'sueldo_total': salario_base
        }

    conceptos_liq = ConceptoLiquidacion.objects.filter(id_liquidacion=liquidacion).select_related('id_concepto')

    bonificaciones = Decimal('0')
    descuentos = Decimal('0')

    nombres_conceptos_cargados = {c.id_concepto.descripcion.lower() for c in conceptos_liq}

    for c in conceptos_liq:
        if c.id_concepto.es_deb_cred:
            bonificaciones += c.monto_concepto
        else:
            descuentos += c.monto_concepto

    # Lógica automática si no se cargaron manualmente
    if 'bonificacion_por_hijos' not in nombres_conceptos_cargados and empleado.hijos_menores_18 > 0:
        concepto_hijos = Concepto.objects.filter(descripcion__iexact='bonificacion_por_hijos').first()
        if concepto_hijos:
            porcentaje = Decimal(concepto_hijos.porcentaje or 0)
            bonificaciones += (salario_base * porcentaje / 100) * empleado.hijos_menores_18

    if 'descuento_ips' not in nombres_conceptos_cargados and empleado.aplica_ips:
        concepto_ips = Concepto.objects.filter(descripcion__iexact='descuento_ips').first()
        if concepto_ips:
            porcentaje = Decimal(concepto_ips.porcentaje or 0)
            descuentos += salario_base * porcentaje / 100

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